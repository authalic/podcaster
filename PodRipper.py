# PodRipper.py
#
# Records an MP3 stream from the KCRW streaming audio feed to an MP3 file.
# Manages the xml and MP3 files to allow for a subscription to the audio files as a podcast.

import urllib
import time
import sys
import tempfile
import os.path
import shutil  # high-level operations on files (copy and removal)
import KCRWscraper  # provides method for obtaining episode description from the KCRW playlist site
from mutagen.mp3 import MP3  # MP3 ID3 Tagging
from mutagen.id3 import TIT2, TPE1, TALB, TYER, TCON  # ID3 Tags


# Requirements:
# Mutagen library, for MP3 tagging
#     get mutagen library at: https://pypi.python.org/pypi/mutagen
# KCRWscraper.py
#     manages the KCRW-specific functions, including obtaining the current URL of the MP3 stream,
#     and obtaining the description of each recorded episode from the online show summary.
# xml (rss) file
#     contains the RSS-compliant XML for use in a podcast subscription application
# HTML document
#     seems to be required by iTunes
# log file
#     created by this application for storing information about activity and crashes

# command line functionality
# $> PodRipper [programname] [duration in minutes]


playlistURL = "http://legacy.kcrw.com/pls/kcrwsimulcast.pls"

# name of program to be recorded
programname = sys.argv[1]  #currently supported:  "MBE" | "Rollins" | "Metropolis"

# length of program to be recorded
ripmin = float(sys.argv[2])
riplength =  ripmin * 60 # length of rip (in seconds)


outputfolder = "/var/www/html/podcast/media/%s/" % (programname)  #MP3 is stored locally here
httppath = "http://192.168.1.198/podcast/media/%s/" % (programname)   #podcast MP3 is served out by web server at this URL
localRSSfile = "/var/www/html/podcast/%s.xml" % (programname)        #XML file containing the local copy of RSS feed

# Log file
logpath = "%slog.txt" % (outputfolder)   #log file stores info on script errors and behavior

# open the log file to append new info
if os.path.exists(logpath):
    logfile = open(logpath, 'a')
else:
    logfile = open(logpath, 'w')

# redirect stderr and stdout to logfile
sys.stderr = logfile
sys.stdout = logfile


# get the URL of the data stream from the playlist file
def getDatastreamURL(playlistURL):
    "Extracts the first URL of an MP3 stream from a playlist file (*.pls) at playlistURL"
    
    playlistFile = urllib.urlopen(playlistURL)
    playlistFileLines = playlistFile.readlines()
    playlistFile.close()

    for line in playlistFileLines:
        if 'http' in line:
            streamURL = line.split('=')[1]
    return streamURL

streamURL = getDatastreamURL(playlistURL)


def getPubDate():
    #create pubDate value for the tag in the RSS file
    pubDate = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    return pubDate
    
pubDate = getPubDate()


def createFilename(programname):

    #create filename datestamp
    today = time.localtime()
    year = today[0]
    month = today[1]
    day = today[2]
    
    #creates filename without extension
    filename = programname + "_" + str(year) + "_" + str(month).zfill(2) + "_" + str(day).zfill(2)
    return filename
 
filename = createFilename(programname)


def createlocalMP3file(filename):

    #creates full path to final locally saved output file, with extension
    localMP3file = outputfolder + filename + ".mp3"
    return localMP3file

localMP3file = createlocalMP3file(filename)


#create a temporary file to store ripped bytes
ripfile = tempfile.NamedTemporaryFile(mode='wb', delete=False)  

#obtain the start time/date of the rip for the RSS feed
itemtitle = time.strftime("%B %d, %Y - %A")               #'July 03, 2007 - Tuesday'

#start ripping

bytestream = urllib.urlopen(streamURL) #open URL from web

starttime = time.time()  # record the start time

logfile.write("Ripping file: " + filename + " at " + time.asctime() + "\n")


while time.time() - starttime < riplength:
    # attempt to rip the specified number of bytes
    
    ripbytes = bytestream.read(20000)  #20000 bytes = 1 sec of recording @ 160kbps
    ripfile.write(ripbytes)


#Problem Here:
# It seems that the stream can hang up, or get dropped here
# when that happens, the loop never reconnects or re-opens the stream.
# there needs to be some kind of check to determine if no bytes were read in the previous time period


# close the temporary file
ripfile.close()
logfile.write("Ripping stopped at " + time.asctime() + "\n")

#copy the temporary file to the permanent MP3 file location on the server

logfile.write("Copying temporary file to final output file\n")

shutil.move(ripfile.name, localMP3file)

#change the permissions of the MP3
os.chmod(localMP3file, 493)  # 493 = 0b111101101

logfile.write("Final MP3 file stored, updating RSS feed\n")


#update the RSS feed
# ***** Consider making this a separate module *****

#format the new item entry

itemurl = httppath + filename + ".mp3"                    #URL of MP3 file on http server

# get today's program information from the KCRW website
programdesc = KCRWscraper.getShowInfo(programname)

# add ID3 tags to the MP3 file

# Podcast naming conventions
# TPE1 - Artist name "The Nerdist", "TWiT", or the hosts, etc.
# TIT2 - Title of individual episode
# TALB - Title of podcast: "Triangulation", "This Week in Tech", etc
# genre: podcast
# media kind: podcast
# description:  show notes
# year

if programname == "MBE":
    TALBname = "Morning Becomes Eclectic"
elif programname == "Rollins":
    TALBname = "Henry Rollins Show"
elif programname == "Metropolis":
    TALBname = "Metropolis"


ID3tag = MP3(localMP3file)
ID3tag["TPE1"] = TPE1(encoding=3, text=["KCRW"])  # artist
ID3tag["TIT2"] = TIT2(encoding=3, text=[itemtitle])  # episode
ID3tag["TALB"] = TALB(encoding=3, text=[TALBname]) # program name
ID3tag["TYER"] = TYER(encoding=3, text=[time.localtime()[0]])  # year
ID3tag["TCON"] = TCON(encoding=3, text=["Podcast"]) # genre
ID3tag.save()


# get the final length of the MP3 file
itemlength = os.path.getsize(localMP3file)                            #size of file in bytes

newitem = '''

      <item>
        <title>%s</title>
        <enclosure
          url="%s"
          length="%i"
          type="audio/mpeg" />
        <itunes:summary>%s</itunes:summary>
        <pubDate>%s</pubDate>
      </item>''' % (itemtitle, itemurl, itemlength, programdesc, pubDate)

#  open RSS file, locate point of insertion, insert new item, save rewritten RSS file

RSS = open(localRSSfile, 'r')
RSSinput = RSS.readlines()
RSS.close()

#store new output text
RSSoutputText = ""

for line in RSSinput:

    if "<!-- INSERTION POINT -->" in line:
        #insert the new item here
        RSSoutputText = RSSoutputText + line + newitem
    else:
        RSSoutputText = RSSoutputText + line

#save the new XML file by writing over the previous file
newRSS = open(localRSSfile, 'w')
newRSS.write(RSSoutputText)
newRSS.close()

logfile.write("XML file updated.\n")
logfile.write("Operation complete at " + time.asctime() + "\n\n\n")

#close the log file and restore stdout and stderr
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
logfile.close()
