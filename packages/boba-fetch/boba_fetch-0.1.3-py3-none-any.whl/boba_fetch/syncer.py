from dataclasses import dataclass
from threading import Event
from multiprocessing import Event as event, Queue
from os import access, R_OK, W_OK
from pathlib import Path
from queue import Empty
import shlex
from subprocess import run, STDOUT, PIPE, SubprocessError
from traceback import format_exc
from typing import Optional, List

from boba_fetch.process import SafeProcess
from boba_fetch.rpc import UnixSocketRPCClient


@dataclass(frozen=True)
class WatchParams:
    host: str
    local_dir: Path
    queue: Queue
    delete: bool
    execute_on_complete: Optional[str] = None


@dataclass(frozen=True)
class SyncParams:
    host: str
    local_dir: Path
    remote_path: Path
    delete: bool
    execute_on_complete: Optional[str] = None

    @property
    def on_complete(self) -> Optional[List[str]]:
        return shlex.split(self.execute_on_complete) if self.execute_on_complete else None

    @property
    def name(self) -> str:
        return self.remote_path.name

    @staticmethod
    def from_watch(watch_params: WatchParams, remote_path: Path) -> 'SyncParams':
        return SyncParams(watch_params.host, watch_params.local_dir, remote_path,
                          watch_params.delete, watch_params.execute_on_complete)


class Syncer:
    def __init__(self, tracker: UnixSocketRPCClient,
                 halt_flag: Optional[Event] = None,
                 temp_dir: Optional[Path] = None):
        self.halt_flag = halt_flag or event()
        self.tracker = tracker
        self.temp_dir = temp_dir
        if self.temp_dir and not self.temp_dir.is_dir():
            raise ValueError(f'Temporary directory {self.temp_dir} does not exist!')
        if self.temp_dir and not access(self.temp_dir, R_OK | W_OK):
            raise ValueError(f'No read-write access to temporary directory: {self.temp_dir}')

    def cmd(self, params: SyncParams) -> List[str]:
        result = ['rsync', '-Pparvzy', '--chmod=u=rw,g=r,o=r']
        if self.temp_dir:
            result += ['-T', str(self.temp_dir)]
        if params.delete:
            result += ['--remove-source-files']
        return result + [f'{params.host}:"{str(params.remote_path)}"', str(params.local_dir)]

    def sync_down(self, params: SyncParams) -> bool:
        proc = SafeProcess(self.cmd(params))
        if not self.halt_flag.is_set():
            for line in proc.run():
                print(f'[{params.remote_path.name}]: {line}')
                self.tracker.check_in(params.name)
                if self.halt_flag.is_set():
                    proc.terminate(3)
        return proc.returncode == 0

    def halt(self):
        self.halt_flag.set()

    def execute_on_complete(self, params: SyncParams) -> None:
        if params.execute_on_complete is not None:
            cmd = params.execute_on_complete.replace('%F', str(params.local_dir / params.name))
            print(f'[{params.name}]: Executing: {cmd}')
            try:
                result = run(shlex.split(cmd), check=False, text=True, stdout=PIPE, stderr=STDOUT)
                print(f'[{params.name}]: ' + result.stdout)
                print(f"[{params.name}]: Exit Code {result.returncode}")
            except SubprocessError:
                print(f"[{params.name}]: Failed to execute on-complete command: {cmd}")

    def watch_queue(self, watch_params: WatchParams):
        while not self.halt_flag.is_set():
            try:
                remote_path = Path(watch_params.queue.get(timeout=5))
                params = SyncParams.from_watch(watch_params, remote_path)
                if not self.tracker.currently_working(params.name):
                    print(f'[{params.name}]: Syncing down: {remote_path} ~> {watch_params.local_dir}')
                    self.tracker.start(params.name)
                    try:
                        self.sync_down(params)
                        if not self.sync_down(params):  # verification
                            print(f"[{params.name}]: Failed to sync down {params.host}:{params.remote_path}")
                            self.tracker.failed(params.name)
                        else:
                            self.tracker.mark_complete(params.name)
                            print(f'[{params.name}]: Sync complete: {params.local_dir / params.name}')
                            self.execute_on_complete(params)
                    except Exception:  # pylint: disable=W0703
                        print(format_exc())
                        print(f"[{params.name}]: Failed to sync down {params.host}:{params.remote_path}")
                        self.tracker.failed(params.name)
            except Empty:
                continue
