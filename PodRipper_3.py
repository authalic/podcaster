'''
PodRipper.py

Author:  Justin Johnson
updated: December 14, 2018

Records an MP3 stream from the KCRW streaming audio feed to an MP3 file.
Manages the xml and MP3 files to allow for a subscription to the audio files as a podcast.

Goals for this version:
    Update to Python 3
    Use Requests module
    Save metadata in a SQLite database
    Use a more appropriate method to generate XML
    Make file management on server easier?
    improve the logging capabilities

'''

import urllib  # <--- use requests instead
import requests
import time
import sys
import tempfile
import os.path
import shutil  # high-level operations on files (copy and removal)
import KCRWscraper_3  # provides method for obtaining episode description from the KCRW playlist site
from mutagen.mp3 import MP3  # MP3 ID3 Tagging
from mutagen.id3 import TIT2, TPE1, TALB, TYER, TCON  # ID3 Tags



class show:

    streamURL = "http://kcrw.streamguys1.com/kcrw_192k_mp3_on_air"  # updated Nov 2016

    def __init__(self):

        # name of program to be recorded
        self.programname = sys.argv[1]  #currently supported:  "MBE" | "Rollins" | "Metropolis"

        # length of program to be recorded
        self.ripmin = float(sys.argv[2])
        self.riplength =  ripmin * 60 # length of rip (in seconds)

        # locations of files on the local server

        #MP3 is stored locally here
        self.outputfolder = "/var/www/html/podcast/media/{}/".format(self.programname)

        #podcast MP3 is served out by web server at this URL
        self.httppath = "http://192.168.1.198/podcast/media/{}/".format(self.programname)

        #XML file containing the local copy of RSS feed
        self.localRSSfile = "/var/www/html/podcast/{}.xml".format(self.programname)        

        # Log file
        self.logpath = "{}log.txt".format(self.outputfolder)   #log file stores info on script errors and behavior

        #obtain the start date/time of the rip
        self.pubDate_str = time.strftime("%B %d, %Y - %A")      #'July 03, 2007 - Tuesday'
        self.pubDate_iso = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())


    def writelog(logmessage):

        # open the log file to write/append new info
        if os.path.exists(self.logpath):
            with open(self.logpath, 'a') as logfile:
                logfile.write(logmessage)
        else:
            with open(self.logpath, 'w') as logfile:
                logfile.write(logmessages)


    def createFilename():
        # get the current date for the show info lookup, in case the date changes before the end of the recording
        # Potential problem:
        # Raspberry Pi must be set to local timezone using raspi-config utility
        today = time.localtime()

        #create filename datestamp
        year = today[0]
        month = today[1]
        day = today[2]
        
        #creates filename without extension
        filename = self.programname + "_" + str(year) + "_" + str(month).zfill(2) + "_" + str(day).zfill(2)
        return filename
 

    def createlocalMP3file():

        #creates full path to final locally saved output file, with extension
        localMP3file = self.outputfolder + self.filename + ".mp3"
        return localMP3file


    def ripstream():
        #create a temporary file to store ripped bytes
        ripfile = tempfile.NamedTemporaryFile(mode='wb', delete=False)  



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
programdesc = KCRWscraper.getShowInfo(programname, today)

# add ID3 tags to the MP3 file

# Podcast naming conventions
# TPE1 - Artist name: "The Nerdist"
# TIT2 - Title of individual episode
# TALB - Title of podcast: "This Week in Tech"
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
itemlength = os.path.getsize(localMP3file) #size of file in bytes


# add the new item to the XML feed
# This should  be done using a framework

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



# redirect stderr and stdout to logfile
sys.stderr = logfile
sys.stdout = logfile

#close the log file and restore stdout and stderr
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__



# testing starts here

if __name__ == '__main__':
    print("testing")

