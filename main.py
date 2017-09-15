import argparse

from srcfile import Srcfile

def validate_i(string):
    try:
        return Srcfile.fromdirectory(string)
    except FileNotFoundError:
        print("Directory not found.")
        return None
    except NotADirectoryError:
        print("Not a directory.")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-directory", default='')
    parser.add_argument("-o", "--output-directory", default='')
    args = parser.parse_args()

    files = validate_i(args.input_directory)
    while not files:
        files = Srcfile.fromdirectory(input("Input file directory: "))

    print(files)
