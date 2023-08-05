class wrdict:
    def __init__(self, d: dict):
        self.d = d

    def __getattr__(self, item: str):
        if isinstance(self.d.get(item), wrdict):
            return self.__class__(self.d.get(item))
        return self.d.get(item)
