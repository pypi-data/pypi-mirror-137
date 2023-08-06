

class File:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self):
        print("entered")
        self._file_cm = open(self.filename, "w+", encoding="utf-8")
        return self._file_cm

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("exited")
        print(exc_type)
        print(exc_value)
        print(exc_traceback)
        if self._file_cm:
            self._file_cm.close()





# with open(filename, "rw+", encoding="utf-8") as file:

with File("something.txt") as file:
    file.write("asd")
