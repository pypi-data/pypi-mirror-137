import os
import asyncio
import warnings
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class PathFlags:
    type_: str  # "file" or "directory"
    mtime: float


class PathWatcher:

    """
    A library that allows you to watch for changes in a list of files or directories.

    Parameters
    ----------
    `callback` : Callable
        A coroutine function with the following signature.

        >>> async def callback(path: str, flag: PathFlags) -> None:
        >>>     print(path, "changed!")
    `paths` : List[str]
        A list of files or directories to watch for changes. Defaults to None which is an empty list.
    `interval` : float
        How many seconds to wait before re-checking again. Defaults to 1.0
    `loop` : asyncio.AbstractEventLoop
        Asyncio event loop. Defaults to the return of "asyncio.get_event_loop()"
    """

    def __init__(self, callback: Callable, paths: List[str] = None, interval: float = 1.0) -> None:
        self.callback = callback
        self.paths = paths if paths else []
        self.interval = interval
        self.loop = asyncio.get_event_loop()

        ########################
        self.path_mappings = {}
        for path in self.paths:
            self.add_path(path)

        self._running = False

    def add_path(self, path: str) -> List[str]:
        """
        Add a new file or directory to the list of paths to be watched.

        Parameters
        ----------
        `path` : str
            Path.

        Returns
        -------
        `List[str]` :
            The newly modified list of paths.
        """

        d = {path: {"last": None, "type": "file" if not os.path.isdir(
            path) else "directory"}}
        self.path_mappings.update(d)
        return list(self.path_mappings.keys())

    def remove_path(self, path: str) -> List[str]:
        """
        Remove a existing file or directory from the list of paths being watched.

        Parameters
        ----------
        `path` : str
            Path.

        Returns
        -------
        `List[str]` :
            The newly modified list of path.
        """

        self.path_mappings.pop(path, None)
        return list(self.path_mappings.key())

    def start(self) -> None:
        """Start the path watcher."""

        if self._running:
            return warnings.warn("Cannot start the path watcher because it is already running. If you meant to stop it, call the stop() method instead.")

        self.loop.create_task(self.__watcher())

    def stop(self) -> None:
        self._running = False

    def get_mtime(self, path: str) -> float:
        if Path(path).is_dir():
            dir_ = Path(path)
            mtimes = [dir_.joinpath(root).joinpath(f).stat(
            ).st_mtime for root, _, files in os.walk(dir_) for f in files]
            return max(mtimes)
        else:
            return os.path.getmtime(path)

    async def __watcher(self) -> None:
        self._running = True
        while self._running:
            for path in list(self.path_mappings.keys()):
                if Path(path).exists():
                    mtime = self.get_mtime(path)
                    last_mtime = self.path_mappings[path].get("last")

                    if last_mtime != mtime:
                        self.path_mappings[path].update({"last": mtime})

                        if last_mtime is not None:
                            flags = PathFlags(self.path_mappings[path]["type"], mtime)
                            await self.callback(path, flags)
            
            await asyncio.sleep(self.interval)
