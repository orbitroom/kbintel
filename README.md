kbintel
=======

Eve Online Killboard Analyzer - **v0.2 ALPHA**

kbintel (killboard intel) is a kill analysis tool primarily suited for reconnaissance and information gathering of hostile forces. 
In it's current alpha version, it is limited to crawling corp/alliance hosted killboards using the [EDK Killboard software](http://www.evekb.org/).
Kbintel is scheduled for a rewrite, which will use the zkillboard api instead; improving data collection speed significantly.
The current version spoofs a user browser and scrapes raw HTML at a rate of 1 page per 2 seconds (configurable). This default rate
has been set to avoid tripping anti-bot measures, but may result in long collection times if crawling a very large organization. 

kbintel outputs a report of the current month's kills with a daily breakdown of the following information:

--------------------------------
Monday, May 5th

Total Kills: 20

Location Breakdown:

    Providence, 9-F0B2 (0.0) - 8
    The Bleak Lands, Huola (0.4) - 7
    Derelik, Sendaya (0.3) - 3
    The Bleak Lands, Kourmonen (0.4) - 1
    Derelik, Futzchag (0.2) - 1

Timeline:

    00:00 - 2
    01:00 - 8
    02:00 - 9
    |
    20:00 - 1

Ships Destroyed:

    Harpy - 3
    Vexor - 3
    Arbitrator - 2
    Capsule - 2
    Cynabal - 1
    Sabre - 1
    Thrasher - 1
    Armageddon Navy Issue - 1
    Exequror - 1
    Blackbird - 1
    Caracal - 1
    Abaddon - 1
    Rupture - 1
    Thorax - 1
--------------------------------

The date and total kills are self-explanitory. The location breakdown is ordered by highest numbers of kills first, and the timeline
shows hourly kills, with gaps to illustrate no-kill hours. And finally, the ships destroyed tally just that. 

**SYNTAX**
----------

To generate a monthly report, simply enter the URL of the killboard's main page from the command line:

_kbintel.py -u URL_
