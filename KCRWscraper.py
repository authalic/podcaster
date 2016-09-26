'''
KCRW program information scraper

Author:  Justin Johnson
rewritten: Jun 21, 2015

This module extracts a daily program description from each day's playlist on KCRW.com
The main method of this module is called at the end of each day's rip, and the description
is written into the XML file for that day's podcast. It then appears in iTunes and on iPods.
'''

import time
import urllib
import json

# get the current date
today = time.localtime()

# extract the year, month, and day as strings
year = str(today[0])
mon = str(today[1]).zfill(2) # pad single-digit months
day = str(today[2]).zfill(2) # pad single-digit days

# build a dictionary of URLs to request the program's playlist info

playlistInfo = {
                "MBE"        : "http://tracklist-api.kcrw.com/Simulcast/date/" + year + "/" + mon + "/" + day + "?program=mb",
                "Rollins"    : "http://tracklist-api.kcrw.com/Simulcast/date/" + year + "/" + mon + "/" + day + "?program=hr",
                "Metropolis" : "http://tracklist-api.kcrw.com/Simulcast/date/" + year + "/" + mon + "/" + day + "?program=mt"
                }


# Extract the program info
# Tracklist API returns a JSON file with show info and track list

def getShowInfo(programName):
    '''Returns the program summary from the KCRW playlist page for the current day's program'''
    
    # use the appropriate URL for the program 
    
    KCRWurl  = urllib.urlopen(playlistInfo[programName])
    KCRWfile = KCRWurl.read()
    KCRWjson = json.loads(KCRWfile)
    KCRWurl.close()
    
    # Get the element values from the JSON object
    # Empty or Null values in the JSON will be converted to None objects
    
    hostname  = KCRWjson[0]["host"]
    guestname = KCRWjson[0]["guest"]
    action    = KCRWjson[0]["action"]
    location  = KCRWjson[0]["location"]
    starttime = KCRWjson[0]["performance_start"]

    # the "live" value seems to be "True" or "False" in the JSON.
    # json module converts "True" to boolean True
    # converts "False" to None
    liveshow = KCRWjson[0]["live"]

    # build the show info string
    # example:  'Hosted by Anne Litt. Surfer Blood Performs Live In Studio at 11:15 AM'
    
    showText = ""
    
    if hostname:
        showText = "Hosted by " + hostname
    
    if guestname:
        showText = showText + ". " + guestname + " " + action + " " + ("Live " if liveshow else "") + location + " at " + starttime
    
    # return a generic description if this operation fails to grab something off the web
    # otherwise, return the full description

    if (showText == "" and programName == "MBE"):
        return "Morning Becomes Eclectic on KCRW"
    elif (showText == "" and programName == "Rollins"):
        return "Henry Rollins Show on KCRW"
    elif (showText == "" and programName == "Metropolis"):
        return "Metropolis on KCRW" 
    else:
        return str(showText)  # convert from Unicode string to String
