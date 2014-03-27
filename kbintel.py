#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import pdb
from sys import platform
from collections import defaultdict, Counter


from clint.textui import colored
from bs4 import BeautifulSoup
from tqdm import *

from common import Browser


# Seconds to wait before each request
TIMEOUT = 2

VERSION = "0.2"

# Instantiates a new browser object with specified timeout variable
browser = Browser(TIMEOUT)


def main():
    parser = argparse.ArgumentParser(description="Killboard Intel - Version: %s" % VERSION)
    parser.add_argument("-u", "--url", help="generate this month's report from url")
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
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
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
            sys.stdout.write("Please respond with 'yes' or 'no' " \
                             "(or 'y' or 'n').\n")


def fetch(url):
    # Helper function to append 'http://' if left off
    if url.find('http://') == -1:
        fetch_url = "http://" + url
    else:
        fetch_url = url

    clear()
    print "Crawler initializing - please wait..."

    # Opens the specified URL and reads the home page
    #home_page = soupify(fetch_url)

    # Parses the URL for the top pilot and 
    #pilot_url = home_page.find_all("table", class_='kb-table awardbox')[0].a['href']
    #pilot_page = soupify(pilot_url)

    # Parse
    #corp_name = pilot_page.find_all('tr', class_='kb-table-row-even')[0].find_all('a')[0].string
    #alliance_name = pilot_page.find_all('tr', class_='kb-table-row-even')[1].find_all('a')[0].string

    #print 'Analyzing {}[{}]'.format(corp_name, alliance_name)

    # Finds the kill page from the main page and feeds it into BeautifulSoup for parsing
    browser.open(fetch_url)
    kill_page = soupify(browser.click_link(text='Kills'))

    # Grab the last page count container and find the number of pages
    page_count = int(kill_page.find_all("div", class_='klsplitter')[-1].find_all('a')[1].string)

    # Prompt for continuation if collection will take longer than 60 seconds
    if page_count >= 100:
        if query_yes_no(str(page_count) + ' pages of data found. Proceed?'):
            collect(kill_page, page_count)
        else:
            print "Exiting"
    else:
        collect(kill_page, page_count)


# BeautifulSoup helper function - returns BS page
def soupify(url):
    browser.open(url)
    return BeautifulSoup(browser.response().read())


def clear():
    # Clears the screen for prettiness
    if platform == "linux" or platform == "linux2":
        return os.system('clear')
    elif platform == "darwin":
        return os.system('clear')
    elif platform == "win32":
        return os.system('cls')



def collect(first_page, pages):
    # Start the crawler on the first page and modify the page variable over iterations
    current_page = first_page

    # Grabs the month
    #pdb.set_trace()
    kill_month = browser.title().split('- ')[1]

    # Grabs the alliance/corp name
    title = current_page.findAll(attrs={"name":"description"})[0]['content'].encode('utf-8').split('- ')[1]

    # Report header
    clear()
    print title + ' - ' + kill_month
    print '\n'

    # Initialize counter variables and data arrays
    next_page_counter = 1
    data_dict = defaultdict(list)

    # Need to preserve date order, which a dictionary can't do
    ordered_keys = []

    for page in tqdm(range(pages), desc='Pages Mined'):
        days = current_page.find_all('div', class_='kb-date-header')
        tables = current_page.find_all('table', class_='kb-table kb-kl-table kb-table-rows')
        for day, table in zip(days, tables):
            if not day.string in ordered_keys:
                ordered_keys.extend([day.string])
            rows = table.tbody.find_all('tr')
            for row in rows:
                kill_location = row.find_all('div', class_='no_stretch kl-location')[0].text
                # Some version use different formatting
                if kill_location.find('\t ') != -1:
                    kill_location = kill_location.split('\t ')[1]
                else:
                    kill_location = kill_location.split('\n')[1]
                kill_time = row.find_all('div', class_='kl-date')[0].text.split('\n')[1]
                kill_data = [kill_location, kill_time]
                data_dict[day.string].append(kill_data)
        # Only increment page number if it's not on the last page
        if next_page_counter < pages:
            next_page_counter += 1
            current_page = soupify(browser.click_link(text='%s' % str(next_page_counter)))
    analyze(data_dict, ordered_keys)


def analyze(data, ordered_keys):
    # Serious unpacking going on - it's like inception up in this b
    for day in ordered_keys:

        kills = data[day]

        kill_locations = []
        kill_times = []

        for kill in kills:
            kill_locations.extend([kill[0]])
            kill_times.extend([kill[1].split(':')[0]])

        kill_counter = Counter(kill_locations)
        time_counter = Counter(kill_times)

        sorted_kills = sorted(kill_counter.items(), key=lambda x: x[1], reverse=True)
        sorted_times = sorted(time_counter.items(), key=lambda x: x)

        index_counter = 0

        print '--------------------------------'
        print str(day)
        print ''
        print 'Total Kills: {}'.format(colored.red(len(kills)))
        print ''
        print 'Location Breakdown: '
        print ''
        for item in sorted_kills:
            print '    ' + str(item[0]) + ' - ' + str(item[1])
        print ''
        print 'Time Breakdown: '
        print ''
        for item in sorted_times:
            print '    {}:00 - '.format(item[0]) + str(item[1])
            # Add space between times if gap exists
            current_hour = int(item[0])
            next_index = (index_counter+1)
            try:
                next_hour = int(sorted_times[next_index][0])
            except IndexError:
                pass
            if (current_hour + 1) < next_hour:
                print ''
            index_counter += 1
            #pdb.set_trace()
        print '--------------------------------'
        print '\n'


if __name__ == '__main__':
    main()