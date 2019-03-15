# casts a date string from an XML feed into a datetime object
# see doc:  https://docs.python.org/3/library/time.html#time.strftime

# date form:  Sat, 9 Mar 2019 01:38:39 -0800

import datetime

datestring = "Sat, 9 Mar 2019 01:38:39 -0800"

d = datetime.datetime.strptime(datestring, '%a, %d %b %Y %H:%M:%S %z')
