'''
KCRW program information scraper

Author:  Justin Johnson
Date:    August 9, 2012
Updated: Feb 6, 2014

This module extracts a daily program description from each day's playlist on KCRW.com
The main method of this module is called at the end of each day's rip, and the description
is written into the XML file for that day's podcast, so it appears in iTunes and on iPods.
'''

import time
import urllib
import re

# get the current date
today = time.localtime()

# extract the year, month, and day as strings
year = str(today[0])
mon = str(today[1]).zfill(2)
day = str(today[2]).zfill(2)

# build a dictionary of URLs to request the program's playlist info

playlistInfo = {       
                "MBE"           : "http://newmedia.kcrw.com/tracklists/index.php?search_type=0&date_from=" + mon + "%2F" + day + "%2F" + year + "&host=Morning+Becomes+Eclectic&date_to=&artist=&channel=Simulcast&label=",
                "Rollins"       : "http://newmedia.kcrw.com/tracklists/index.php?search_type=0&date_from=" + mon + "%2F" + day + "%2F" + year + "&host=Henry+Rollins&date_to=&artist=&channel=Simulcast&label=",
                "Metropolis"    : "http://newmedia.kcrw.com/tracklists/index.php?search_type=0&date_from=" + mon + "%2F" + day + "%2F" + year + "&host=Metropolis&date_to=&artist=&channel=Simulcast&label="
                }

# Extract the program info from the playlist HTML file using a blunt method
# Read the entire HTML file
# look for the <span id = "showTab"> tag
# extract the contents of those tags and strip out any HTML tags 

def findSpan(KCRWlines, programName):
    '''Search a list of lines from an HTML file
    Return the block of HTML containing the program info'''

    span = ""
    spanCount = 0
    
    # this method looks specifically for the substring '<span id="showTab">'
    # if that spelling is altered in any way, this method will fail
    
    for line in KCRWlines:
        if (('<span id="showTab">' in line and spanCount == 0) or (spanCount > 0)):
            span = span + line
            spanCount += len([m.start() for m in re.finditer("<SPAN", line.upper())])
            spanCount -= len([m.start() for m in re.finditer("</SPAN", line.upper())])
    
        # remove the words "LISTEN" and "WATCH" which might get included at the end of some descriptions
        
        if ("LISTEN" in span or "WATCH" in span):
            span = span[:min(span.find("LISTEN"), span.find("WATCH"))]
        
    # return a generic description if this operation fails to grab something off the web
    
    if (span == "" and programName == "MBE"):
        return "Morning Becomes Eclectic on KCRW"
    elif (span == "" and programName == "Rollins"):
        return "Henry Rollins Show on KCRW"
    elif (span == "" and programName == "Metropolis"):
        return "Metropolis on KCRW" 
    else:
        return span


def stripTags(htmlcode):
    '''Strips all HTML tags from a string using regular expression'''
    
    return re.sub('<[^<]+?>', '', htmlcode).strip()


def getShowInfo(programName):
    '''Returns the program summary from the KCRW playlist page for the current day's program'''
    
    # use the appropriate URL for the program.
    
    KCRWfile = urllib.urlopen(playlistInfo[programName])
    KCRWlines = KCRWfile.readlines()
    KCRWfile.close()

    showTab = findSpan(KCRWlines, programName)

    showText = stripTags(showTab)

    return showText

