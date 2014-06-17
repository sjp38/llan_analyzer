#!/usr/bin/env python

""" Entry point for analyzer execution """

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"

import sys

import anal
import parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: %s <program source code path>" % sys.argv[0]
        exit(1)
    result = anal.analyze(parser.parse_file(sys.argv[1]))
    print "[RESULT]"
    for key in sorted(result.keys()):
        print "%s: %s" % (key, result[key])
        if result[key].type_ == anal.TOP:
            print "\tDangerous! This may not end in reasonable time!!"
