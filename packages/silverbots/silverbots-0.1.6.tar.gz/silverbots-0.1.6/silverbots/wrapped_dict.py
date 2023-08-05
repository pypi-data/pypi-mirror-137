class wrdict:
    def __init__(self, d: dict):
        self.d = d

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, item: str):
        if isinstance(self.d.get(item), dict):
            return self.__class__(self.d.get(item))
        return self.d.get(item)

    def __repr__(self):
        return self.d.__repr__()
