import os, re, subprocess
from sys import argv

class FieldMismatch(Exception):
    pass

class Field:
    def __init__(self, index, values, guess=None):
        self.index = index
        # integer
        self.values = values
        # set
        self.guess = guess
        # string
        self.confirmed = False

    CRC32 = re.compile(r'[A-Fa-f0-9]{8}')
    TYPE = re.compile(r'(720|1080|TV|BD|FLAC|AAC|AC3)')

class Brackets:
    pairs = {'[':']', '(':')'}
    
    def listleft():
        return list(Brackets.pairs.keys())
    def listright():
        return list(Brackets.pairs.values())
    def listall():
        return Brackets.listleft() + Brackets.listright()
    def stringleft():
        return ''.join(Brackets.listleft())
    def stringright():
        return ''.join(Brackets.listright())
    def stringall():
        return ''.join(Brackets.listall())
    def findleft(string):
        for char in string:
            if char in Brackets.listleft():
                return string.index(char)
        return -1

def enumerateinputs(path):
    path = path.rstrip('/\\')
    try:
        result = [os.path.join(path, f) for f in os.listdir(path)]
    except FileNotFoundError as e:
        raise e
    result = filter(lambda s: s.endswith('.mkv') and os.path.isfile(s), result)
    return list(result)

def debracket(string):
    string = string.strip()

    if string == '':
        return []
    elif not any(bracket in string for bracket in Brackets.listleft()):
        return [string]
    elif any(string.startswith(bracket) for bracket in Brackets.listleft()):
        # [('result', '['), *debracket('leftover')] 
        #     where debracket('[result]leftover')
        brackettype = string[0]
        parts = string[1:].partition(Brackets.pairs[brackettype])
        return [(parts[0], brackettype), *debracket(parts[2])]
    else:
        index = Brackets.findleft(string)
        return [string[:index].strip(), *debracket(string[index:])]

def parsenames(pathlist):
    filenames = [os.path.split(name)[1].rpartition('.')[0] for name in pathlist]
    # .mkv should be assumed
    splitnames = [debracket(name) for name in filenames]
    if len(set(map(len, splitnames))) > 1:
        raise FieldMismatch("File names too different: field quantity")

    fields = []
    for index, item in enumerate(splitnames[0]):
        if type(item) == type(()):
            examples = set(ex[index][0] for ex in splitnames)
            if index == 0 and len(examples) == 1:
                fields.append(Field(index, examples, guess="group"))
                continue
            elif item[1] == '[' and Field.CRC32.fullmatch(item[0]):
                fields.append(Field(index, examples, guess="hash"))
                continue
            elif Field.TYPE.search(item[0]):
                fields.append(Field(index, examples, guess="quality"))
                continue
            else:
                fields.append(Field(index, examples))
                continue
        elif type(item) == type(''):
            examples = set(ex[index] for ex in splitnames)
            if index < 2 and len(examples) > 1:
                fields.append(Field(index, examples, guess="main"))
                continue
            else:
                fields.append(Field(index, examples))
                continue
        else:
            raise TypeError("Found {} while expecing str or tuple".format(
                type(item)))

    confirmed_fields = []
    for field in fields:
        print("Field {} contains these unique values:".format(field.index))
        [print(x) for x in field.values] #good practice?
        while True:
            if field.guess:
                user = input("Field name? (default={}): ".format(field.guess))
                if user == '':
                    user = field.guess
            else:
                user = input("Field name?: ")

            if user == '' or user in confirmed_fields:
                print("Please provide a unique field name.")
            else:
                confirmed_fields.append(user)
                field.guess = user
                field.confirmed = True
                break

    return fields

def mkformat(fields):
    # ask for order
    # verify compatibility
    # return... regex?
    pass

def mapper(pathlist, format):
    # return mapping
    pass

def processcontroller(processes=5):
    # dispatch processes and make stdout reasonable
    pass

if __name__ == "__main__":
    if len(argv) < 2:
        # interactive mode
        while True:
            indir = input("Input directory: ")
            if os.path.isdir(indir):
                break
            else:
                print("Not a directory. Try again.")

        inputnames = enumerateinputs(indir)
        
        fields = parsenames(inputnames)

        outformat = mkformat(fields)
        mapping = mapper(inputnames, outformat)

        processcontroller(mapping)

    if len(argv) < 3:
#        print(argv)
        inputnames = enumerateinputs(argv[1])
#        [print(x) for x in inputnames]
        fields = parsenames(inputnames)
        [print(x.index, x.guess, x.values) for x in fields]

    else:
        print("I don't know what you're saying.")
