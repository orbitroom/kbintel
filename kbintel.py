#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Killboard Intel

Usage:
  kbintel.py URL [-v] [-d]
  kbintel.py -h | --help
  kbintel.py --version

Options:
  -v --verbose  Show more text.
  -d --debug    Show debug messages.
  -h --help     Show this screen.
  --version     Show version.

"""

import sys
import os
import sqlite3
import ConfigParser
from docopt import docopt
import zkb
import pdb


# Read config vars from config.ini
conf = ConfigParser.ConfigParser()
conf.read("config.ini")
db_schema = conf.get("GLOBAL", "db_name")

# Set global vars
VERSION = "0.3"
cursor = None
db = None
verbose = False
debug = False


# Set global vars based on args
def set_globals():
    global verbose, debug
    if arguments['--verbose']:
        verbose = True
    if arguments['--debug']:
        print arguments


# Initialize database connection
def db_init():
    # TODO: Add search functionality to dynamically find db
    # TODO: Add option to automatically download latest sqlite3 db
    # TODO: Add print statements to log
    global cursor, db, verbose

    # Validate if path in config points to a file
    if os.path.isfile(db_schema):
        try:
            db = sqlite3.connect(db_schema)
            cursor = db.cursor()
            if verbose:
                print "DB connection:\tGOOD"
        except Exception, e:
            print e
            sys.exit(2)
    else:
        # TODO: Implement optional db connection - simple mode
        sys.exit("SQLite Database Not Found! Verify path in config.ini")


# I know, total overkill
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'\n" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def validate(url):
    # Check for zKillboard patterns if non-standard URL
    if '.' not in url:
        print "validate short url"
    # Make sure URL points to zKillboard only
    elif 'zkillboard.com' in url:
        print "zKillboard URL"
    else:
        print "INVALID URL"
        sys.exit()


def clear():
    # Clears the screen for prettiness
    os.system('clear')


if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    set_globals()
    db_init()
    validate(arguments['URL'])
    #pdb.set_trace()