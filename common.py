import mechanize
import time
from bs4 import BeautifulSoup


class Browser(mechanize.Browser):
    """
    Browser customized for kbintel. This includes
    ignoring robots.txt, sending a chrome-on-desktop
    user-agent, and observing rate-limiting.
    """
    def __init__(self, rate, history=None, request_class=None):
        """
        Create a browser which observes the specified rate-limit.
        rate: time in seconds. wait this period of time before
        actually performing any function which makes a
        connection.
        """
        mechanize.Browser.__init__(self,history,request_class)
        self.rate = rate #in seconds
        self.addheaders = [("User-agent", "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36")]
        self.set_handle_robots(False)

    def set_rate(self, rate):
        self.rate = rate

    """
    functions we must override:
    open
    open_novisit
    reload
    back (not always?...)
    follow_link
    submit
    retrieve
    """
    def open(self, url, data=None, timeout=None):
        time.sleep(self.rate)
        return mechanize.Browser.open(self, url, data, timeout)

    # timeout=None: hopefully the super function should
    # take care of this
    def open_novisit(self, url, data=None, timeout=None):
        time.sleep(self.rate)
        return mechanize.Browser.open_novisit(self, url, data, timeout)

    def follow_link(self, link=None, **kwds):
        time.sleep(self.rate)
        return mechanize.Browser.follow_link(self, link, **kwds)

    def submit(self, *args, **kwds):
        time.sleep(self.rate)
        return mechanize.Browser.submit(self, *args, **kwds)

    def back(self, n=1):
        time.sleep(self.rate)
        return mechanize.Browser.back(self, n)