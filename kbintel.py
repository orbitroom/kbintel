#!/usr/bin/env python

import sys
import os
import time
import argparse
from bs4 import BeautifulSoup
from tqdm import *
from common import Browser
import pdb

# Seconds to wait before each request
TIMEOUT = 2

# Instantiates a new browser object with specified timeout variable
browser = Browser(TIMEOUT)

def main():
    parser = argparse.ArgumentParser(description="Killboard Intel")
    parser.add_argument("-u", "--url", help="fetch intel from url")
    args = parser.parse_args()

    if args.url:
        fetch(args.url)
    else:
        parser.print_help()


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
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
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


def fetch(url):
    # Helper function to append 'http://' if left off
    if url.find('http://') == -1:
        fetch_url = "http://"+url
    else:
        fetch_url = url

    # Clears the screen for prettiness
    os.system('clear')
    print "Retrieving data - please wait..."

    # Opens the specified URL and reads the home page
    home_page = soupify(fetch_url)
    
    # Parses the URL for the top pilot and 
    pilot_url = home_page.find_all("table", class_='kb-table awardbox')[0].a['href']
    pilot_page = soupify(pilot_url)

    # Parse
    corp_name = pilot_page.find_all('tr', class_='kb-table-row-even')[0].find_all('a')[0].string
    alliance_name = pilot_page.find_all('tr', class_='kb-table-row-even')[1].find_all('a')[0].string

    print 'Analyzing {}[{}]'.format(corp_name, alliance_name)
    
    # Finds the kill page from the main page and feeds it into BeautifulSoup for parsing
    browser.click_link(text='Home')
    kill_page = soupify(browser.click_link(text='Kills'))
    
    # Counts the number of pages to parse
    page_count = int(kill_page.find_all("div", class_='klsplitter')[0].find_all('a')[1].string)

    estimate = (TIMEOUT*page_count)

    # Prompt for continuation if collection will take longer than 60 seconds
    if estimate >= 60:
        if query_yes_no(page_count + ' page_count of history found. Report generation will take ~'
                        + str(estimate) + ' seconds. Continue?'):
            collect(kill_page, page_count)
        else:
            print "Exiting"
    else:
        collect(kill_page, page_count)


# BeautifulSoup helper function - returns BS page
def soupify(url):
    browser.open(url)
    return BeautifulSoup(browser.response().read())


def collect(first_page, page_count):
    print "Generating Report"
    #pdb.set_trace()
    for page in tqdm(range(page_count), desc='Pages mined:'):
        time.sleep(2)

if __name__ == '__main__':
    main()