from pathlib import Path
from time import time
from typing import Optional, Dict, List

from boba_fetch.rpc import UnixSocketRPCServer


class Tracker(UnixSocketRPCServer):
    def __init__(self, directory: Path, check_in_timeout: float = 5.0) -> None:
        self.working: Dict[str, float] = {}
        self.directory = directory
        self.timeout = check_in_timeout
        if not self.directory.is_dir():
            self.directory.mkdir(parents=True, exist_ok=True)
        UnixSocketRPCServer.__init__(self)

    @UnixSocketRPCServer.serve
    def completed_at(self, name: str) -> float:
        if (self.directory / name).is_file():
            contents = (self.directory / name).open().read().strip()
            return float(contents) if contents.replace('.', '', 1).isdigit() else 0.0
        else:
            return 0.0

    @UnixSocketRPCServer.serve
    def mark_complete(self, name: str, timestamp: Optional[float] = None) -> None:
        (self.directory / name).open('w+').write(str(timestamp or time()))
        self.not_working(name)

    @UnixSocketRPCServer.serve
    def newer_than(self, name: str, timestamp: float) -> bool:
        return self.completed_at(name) >= timestamp

    @UnixSocketRPCServer.serve
    def start(self, name: str) -> None:
        self.check_in(name)
        (self.directory / name).open('w+').write('')

    @UnixSocketRPCServer.serve
    def failed(self, name: str) -> None:
        (self.directory / name).unlink(missing_ok=True)
        self.not_working(name)

    def not_working(self, name: str) -> None:
        if name in self.working:
            del self.working[name]

    def clean(self) -> None:
        now = time()
        for name in [n for n, c in self.working.items() if now - c >= self.timeout]:
            self.failed(name)

    @UnixSocketRPCServer.serve
    def check_in(self, name: str) -> None:
        self.clean()
        self.working[name] = time()

    @UnixSocketRPCServer.serve
    def currently_working(self, name: str) -> bool:
        return name in self.working and time() - self.working[name] <= self.timeout

    @UnixSocketRPCServer.serve
    def unfinished(self) -> List[str]:
        self.clean()
        return [n for n in self.working]
