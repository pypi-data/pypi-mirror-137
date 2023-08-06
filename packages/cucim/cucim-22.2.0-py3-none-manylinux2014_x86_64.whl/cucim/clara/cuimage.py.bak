from . import _cucim

class CuImage:
    def __init__(self, *args, **kwargs):
        self._C = _cucim.CuImage(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self._C, attr)

    def __setattr__(self, attr, val):
        if attr == '_C':
            object.__setattr__(self, attr, val)
        else:
            setattr(self._C, attr, val)

    def read_region(self, *args, **kwargs):
        region = self._C.read_region(*args, **kwargs)
        print("@@@", region.__class__)
        print("@@@", self.__class__)
        return region
