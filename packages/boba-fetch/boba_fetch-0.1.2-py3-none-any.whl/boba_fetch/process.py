from functools import partial
from multiprocessing import Event as event
from subprocess import Popen, TimeoutExpired, STDOUT, PIPE
from typing import List, Optional, Iterator


class SafeProcess:
    def __init__(self, cmd: List[str]) -> None:
        self.cmd = cmd
        self.proc: Optional[Popen] = None
        self.started = event()

    def run(self) -> Iterator[str]:
        self.proc = Popen(self.cmd, stderr=STDOUT, stdout=PIPE)
        self.started.set()
        while self.proc.stdout is not None and self.proc.poll() is None:
            line = []
            for byte in iter(partial(self.proc.stdout.read, 1), b''):
                if byte not in {b'\n', b'\r', b''}:
                    line.append(byte.decode())
                else:
                    yield ''.join(line)
                    line = []

    @property
    def returncode(self) -> Optional[int]:
        return self.proc.returncode if self.proc else None

    def terminate(self, timeout: int = 10) -> None:
        if self.proc is not None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout)
            except TimeoutExpired:
                self.proc.kill()
