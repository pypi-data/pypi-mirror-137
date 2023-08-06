class TelegramType:
    def __init__(self, scopes):
        for x in scopes:
            self.__setattr__(x[0], x[1])
        self._view = self.__dict__.copy()

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{x[0]}={x[1]}" for x in self._view.items() if x[1] is not None]) + ")"
