#!/usr/bin/env python

"""llan parser"""

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2014, SeongJae Park"
__license__ = "GPLv3"

import sys

# Make raw expression(python string) to list(python list with strings)
def parse(expr, depth = 1):
    if not expr.startswith("[") and depth == 1:
        expr = "[" + expr + "]"
    list_ = []
    atom = ""
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == "[":
            sublist, sublen = parse(expr[i + 1:], depth + 1)
            i = i + sublen
            if depth == 1:
                return sublist
            list_.append(sublist)
        elif c == "]":
            if atom != "":
                list_.append(atom)
                atom = ""
            return list_, i + 1
        elif c == " ":
            if atom != "":
                list_.append(atom)
            atom = ""
        else:
            atom = atom + c
        i = i + 1

def print_program(program, depth=1):
    i = 0
    indent = ''
    while (i < depth * 2):
        indent += ' '
        i += 1
    for atom in program:
        if isinstance(atom, list):
            print indent + "["
            print_program(atom, depth + 1)
            print indent + "]"
        else:
            print indent + atom

def parse_file(file_path):
    with open(sys.argv[1], 'r') as f:
        program = []
        statement = ""
        block = False
        in_block = False
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]

            if block:
                in_block = True

            if len(line) < 1:
                continue
            elif not block and line[-1] == '[':
                block = True
            elif block and line == ']':
                block = False
                in_block = False

            if in_block:
                if line.split() == [']']:
                    line = line + ']'
                elif line.split() == [']', '[']:
                    pass
                elif line[-1] == '[':
                    line = '[' + line
                else:
                    line = '[' + line + ']'

            statement += line
            if not block and statement != "":
                parsed = parse(statement)
                program.append(parse(statement))
                statement = ""
    return program

if __name__ == "__main__":
    parse_file(sys.argv[1])
