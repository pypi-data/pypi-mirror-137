class wrdict:
    def __init__(self, d: dict):
        self.d = d

    def __getattr__(self, item: str):
        return self.__class__(self.d.get(item))
