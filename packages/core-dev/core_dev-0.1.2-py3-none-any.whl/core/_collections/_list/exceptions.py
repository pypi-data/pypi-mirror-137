


class ListException(Exception):
    def __init__(self, message="", exception_type="ListException") -> None:
        self.message = message
        self.exception_type = exception_type

    def __str__(self):
        return f"<{self.__class__.__name__} message='{self.message}''>"


class EmptyListError(ListException):
    def __init__(self, message="", exception_type="EmptyListError") -> None:
        super().__init__(message, exception_type)



if __name__ == '__main__':
    test = EmptyListError("test")
    print(test)
