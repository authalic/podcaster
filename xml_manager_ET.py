import xml.etree.ElementTree as ET  # doc: https://docs.python.org/3/library/xml.etree.elementtree.html
import datetime
from datetime import timedelta

# this will be a module
# functions will include
# get the current xml feed
# create a new item in the feed for the new podcast episode
# delete any items from the xml feed older than x number of days


def expired(item):
    '''if item is older than the number of days in expiredays, return True'''

    expiredays = 14  # number of days after which an item will be deleted from the xml

    if datetime.date.today() - item > timedelta(days=expiredays):
        return True
    else:
        return False



xmlfile = 'testfeed.xml'

tree = ET.parse(xmlfile)  # parse the xml file into an ElementTree
root = tree.getroot()  # get the root of the tree
chan = root[0]  #  'channel' is the first element under the root
items = chan.findall('item')

for item in items:
    title = item.find('title').text
    pubdate_str = item.find('pubDate').text
    pubdate = datetime.datetime.strptime(pubdate_str, '%a, %d %b %Y %H:%M:%S %Z')

    print(pubdate, expired(pubdate.date()))  # pubdate.date() extracts the date from a datetime obj
