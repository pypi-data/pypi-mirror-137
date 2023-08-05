import sys
from pathlib import Path
import inspect


class _PathAdder:
    def __init__(self):
        self.parents = self._parents()

    def _parents(self):
        for frame in inspect.stack()[3:]:
            path = frame.filename
            if not path.startswith("<frozen "):
                return Path(path).parents
        return []

    def try_insert_name(self, name):
        for parent in self.parents:
            path = parent / name
            if path.exists():
                path_ = str(path)
                try:
                    sys.path.remove(path_)
                except ValueError:
                    pass
                sys.path.insert(0, path_)

                return


path_adder = _PathAdder()
path_adder.try_insert_name("src")
