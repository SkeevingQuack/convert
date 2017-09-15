from pathlib import Path
import os, re

class Srcfile:
    @classmethod
    def fromdirectory(cls, dir):
        path = Path(dir).resolve(strict=True)
        if not path.is_dir():
            raise NotADirectoryError
        infiles = []
        for child in path.iterdir():
            if child.is_file() and child.suffix == '.mkv':
                infiles.append(cls(child))
        return infiles
                
    def __init__(self, path):
        self.src = path
        self.dest = None
        self.fields = None

    def __str__(self):
        result = self.src.name
        if self.dest:
            result += " --> " + self.dest.name
        return result


    
    def debracket(self):
        bracketmap = {'[':']', '(':')'}
        leftbrackets = list(bracketmap.keys())
        return _debracket_internal(self.src.name[:-4], bracketmap, leftbrackets)


def _debracket_internal(string, bracketmap, leftbrackets):
    string = string.strip()
    if string == '':
        return []
    elif not any(bracket in string for bracket in leftbrackets):
        return [string]
    elif any(string.startswith(bracket) for bracket in leftbrackets):
        brackettype = string[0]
        parts = string[1:].partition(bracketmap[brackettype])
        return [(parts[0], brackettype), *_debracket_internal(parts[2], bracketmap, leftbrackets)]
    else:
        match = re.search(r'[\[\(]', string)
        #TODO: compile?
        index = match.span()[0]
        #TODO: deal with the None TypeError
        return [string[:index].strip(), *_debracket_internal(string[index:], bracketmap, leftbrackets)]
