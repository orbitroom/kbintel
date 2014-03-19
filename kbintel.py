#!/usr/bin/env python

import sys
import argparse
import bs4 as BeautifulSoup
from common import Browser


def main():
    parser = argparse.ArgumentParser(description="Killboard Intel")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-u", "--url", help="fetch intel from url")
    args = parser.parse_args()

    if args.verbose:
        print "\nVerbosity Enabled"
        print "Running '{}'".format(__file__)
    elif args.url:
        fetch(args.url)
    else:
        parser.print_help()


def fetch(url):
    fetch_url = url
    if url.find('http://') == -1:
        fetch_url = "http://"+url

    br = Browser(10)
    br.open(fetch_url)

    print br.title()

if __name__ == '__main__':
    main()