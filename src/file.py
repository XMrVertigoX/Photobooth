import os

class File():
    def __init__(self, path):
        self.basename, self.extension = os.path.splitext(path)

    def exits():
        return os.path.exists(self.basename + self.extension)

    def getBasename(self):
        return self.basename

    def getExtension(self):
        return self.extension

    def getAbsolutePath(self):
        return os.path.abspath(self.basename + self.extension)

    def copy(self, location):
        pass

    def move(self, location):
        pass