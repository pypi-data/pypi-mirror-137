import mrcfile


class Map:
    def __init__(self, file_name, lazy=True):
        self._file_name = file_name
        self._lazy = lazy
        self._map = None
        if not lazy:
            self._map = mrcfile.open(self._file_name)

    @property
    def file_name(self):
        return self._file_name

    def read(self):
        print(f"opening {self._file_name}...")
        self._map = mrcfile.open(self._file_name)