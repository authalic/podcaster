'''
KCRW program information scraper

Author:  Justin Johnson
updated: May 18, 2018

This module extracts a daily program information from KCRW.com
The main method of this module is called at the end of each day's rip.
The host name and playlist are written into the XML file for that day's podcast episode.
'''

import requests
# Extract the program info

def getShowInfo(programName, today):
    '''Returns the program summary from the KCRW playlist page''''

    # extract the year, month, and day as strings
    year = str(today[0])
    mon = str(today[1]).zfill(2)  # pad single-digit months
    day = str(today[2]).zfill(2)  # pad single-digit days

    # start times are used to filter the program's playlist from the full-day playlist
    starttimes = {
        "MBE": "09:00",
        "Metropolis": "22:00",
        "Rollins": "20:00"
    }

    # Tracklist API returns a JSON file with show info and track list
    # get the complete tracklist from the specified date
    alltracklist = requests.get("http://tracklist-api.kcrw.com/Simulcast/date/" + year + "/" + mon + "/" + day).json()

    # filter out the tracks for the program, using the appropriate 'program_start' key value
    tracklist = [track for track in alltracklist if track['program_start'] == starttimes[programName]]

    playlist = ""

    # create a playlist line containing the start time, artist, and trackname for each track
    for track in tracklist:
        if "BREAK" in track['artist']:
            playlist += track['time'] + "  - BREAK -" + "\n"
        elif track['label'] == "KCRW Live":
            playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + " [Live @ KCRW]\n"
        else:
            playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + "\n"


    # build the show info string
    # example:  'Hosted by Anne Litt' + list of tracks

    showText = ""

    # get the name of the episode host
    if tracklist[0]["host"]:
        showText = "Hosted by " + tracklist[0]["host"] + "\n\n"

    if playlist:
        showText += playlist

    # return a generic description if this operation fails to grab something off the web
    if (showText == "" and programName == "MBE"):
        return "Morning Becomes Eclectic on KCRW"
    elif (showText == "" and programName == "Rollins"):
        return "Henry Rollins Show on KCRW"
    elif (showText == "" and programName == "Metropolis"):
        return "Metropolis on KCRW"

    # otherwise, return the full description
    if showText:
        return str(showText)  # convert from Unicode string to String

    # if you get here, no show info was obtained
    return "Unable to obtain show info"
