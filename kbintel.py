#!/usr/bin/env python

import sys
import argparse
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc)


def main():
    parser = argparse.ArgumentParser(description="Killboard Intel")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-l", "--location", help="lookup by location")
    args = parser.parse_args()

    if args.verbose:
        print "\nVerbosity Enabled"
        print "Running '{}'".format(__file__)
    elif args.location:
        lookup(args.location)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()