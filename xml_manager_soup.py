import requests
from bs4 import BeautifulSoup

# get the xml feed of the top 10 podcasts on iTunes
xmlfeed = 'https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/10/explicit.rss'

# convert the response to text
xmlfile = requests.get(xmlfeed).text

# convert to a beautifulsoup object
soup = BeautifulSoup(xmlfile, 'xml')

# d = datetime.datetime.strptime(soup.lastBuildDate.string, '%a, %d %b %Y %H:%M:%S %z')

# loop through the podcasts (item objects)
items = soup.find_all('item')

for item in items:
    print(item.title.string)
