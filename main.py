#!/usr/bin/env python

import sys

import anal
import parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <program source code path>"
        exit(1)
    result = anal.analyze(parser.parse_file(sys.argv[1]))
    print "[RESULT]"
    for key in result.keys():
        print "%s: %s" % (key, result[key])
