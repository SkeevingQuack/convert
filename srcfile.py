from pathlib import Path
import os

class Srcfile:
    @classmethod
    def fromdirectory(cls, dir):
        path = Path(dir).resolve(strict=True)
        infiles = []
        for child in path.iterdir():
            if child.is_file() and child.suffx == '.mkv':
                infiles.append(cls(child))

    def __init__(self, path):
        self.src = path
        self.dest = None
        self.fields = None

    def __str__(self):
        result = self.src.name
        if self.dest:
            result += " --> " + self.dest.name
        return result
