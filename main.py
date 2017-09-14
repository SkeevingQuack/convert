import argparse

from srcfile import Srcfile

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-directory")
parser.add_argument("-o", "--output-directory")
args = parser.parse_args()

if args.input_directory:
    files = Srcfile.
