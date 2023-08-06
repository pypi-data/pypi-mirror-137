

class DictException(Exception):
    def __init__(self, message=""):
        self.message = message

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} message='{self.message}''>"


class EmptyDictError(DictException):
    pass