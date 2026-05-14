#! /usr/bin/env python3

import getopt
import sys

from member_copy import member_copy


def main(argv):
    inputfile = ""
    outputfile = ""
    members = []

    opts, _args = getopt.getopt(argv, "hi:o:m:", ["ifile=", "ofile=", "member="])
    for opt, arg in opts:
        if opt == "-h":
            print("copy_members.py -i <inputfile> -o <outputfile> -m <member>")
            return 0
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-m", "--member"):
            members.append(arg)

    print("Input file is ", inputfile)
    print("Output file is ", outputfile)
    print(f"Member List {members}")

    if not inputfile or not outputfile or not members:
        print("Input file, output file, and at least one member are required.")
        return 8

    return member_copy(inputfile, outputfile, members)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
