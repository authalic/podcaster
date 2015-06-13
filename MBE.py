
#MBE 3.2
#revision history:
#  1.0  used an external application (stationripper.exe) to rip the MP3 stream to a file
#       which was then uploaded into iTunes.  When KCRW changed their MP3 stream to include
#       ID3 tags, stationripper stored each song as a separate MP3 file, instead of a single
#       file for each day's episode, which made the daily podcast fail.
#  2.0  abandoned stationrippper, and used Python to open the MP3 stream directly and store
#       it as a file.  Each file was uploaded into iTunes as before.  The problem with this
#       approach arose from the fact that KCRW uses a variable bitrate (VBR) stream in order
#       to transmit audio data most efficiently.  The MP3 stream was stored without any kind
#       of file header, which caused iTunes to greatly miscalculate the length of each day's
#       file.
#  3.0  iTunes looks for a Xing header, which contains data on the number of frames in an
#       MP3 file, the number of bytes, and a "lookup" table which assists applications in
#       players in zooming around to a particular point in time in a file.  This revision
#       adds code that can create this Xing header and prepend it to the MP3 file.
#  3.1  Added error handling, to prevent the entire application from crashing if any one of
#       connections to the URL timed out.  Avoids the need to code a buffer. Also implemented
#       a log file, to record any error messages encountered by the program as it rips. Any
#       time-out error message or unhandled error message will be stored in the file. 
#  3.2  Implemented a few changes, August 2012.  
#       Broke code up into more functions, so it's not quite as sequential at the Global level.  
#       Added ID3 tags to the MP3 file.  Added code to scrape the daily program description from
#       the KCRW playlist page at the end of the rip, and save that in the podcast XML file.  
#       Generally tried to make the code more modular, in preparation for version 4.0 changes.
#
# Problem history: 
# Sep-Oct 2010 interruption
# Seemed to be the result of connectivity problems, unsure exactly as to where.
# Implemented exception handling to permit the application to continue in the event of a
#   network time-out error
# 
# Apr-May 2011 interruption
# Files are garbled. Lots of invalid frame (approx 50%).  The raw MP3 stream works.
# Some error exists in the processing segment: myMP3.ParseFrames()
# The KCRW feed is no-longer VBR.  The VBR processing might be messing something up



import urllib
import time
import sys
import traceback
import shutil
from os.path import getsize
import myMP3  #IMPORTANT: Contains a whole shitload of code
import MBEscraper  # provides method for obtaining daily program info from the KCRW playlist site
from mutagen.mp3 import MP3  # ID3 Tagging
from mutagen.id3 import TIT2, TPE1, TALB, TYER, TCON  # ID3 Tagging

 
# Log file
logpath = "C:/htdocs/podcast/MP3log.txt" #log file stores info on script errors and behavior
logfile = open(logpath, 'a')             #open the log file to append new info

# redirect stderr and stdout to logfile
sys.stderr = logfile
sys.stdout = logfile


programname = "MBE"
playlistURL = "http://legacy.kcrw.com/pls/kcrwsimulcast.pls"

riplength =  10800 #3 hours (in seconds)

outputfolder = "C:/htdocs/podcast/media/MBE/"    #MP3 is stored locally here
httppath = "http://localhost/podcast/media/MBE/" #podcast MP3 is served out by web server at this URL
rssfeed = "C:/htdocs/podcast/mbe.xml"            #XML file containing the local copy of RSS feed


# get the URL of the data stream from the playlist file
def getDatastreamURL(playlistURL):
    "Extracts the URL of an MP3 stream from a playlist file *.pls at playlistURL"
    
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
    

def createFullname(filename):

    #creates full path to local file, with extension
    fullname = outputfolder + filename + ".mp3"
    
    return fullname

fullname = createFullname(filename)



def createTempFilename(outputfolder):
    
    #store ripped file with a temporary name first, change it to fullname after post-processing
    tempname = outputfolder + "temp.mp3"
    
    return tempname

tempname = createTempFilename(outputfolder)



#start ripping

bytestream = urllib.urlopen(streamURL) #open URL
outputfile = open(tempname, 'wb')      #open local file for storage of bitstream

starttime = time.time()  # record the start time

logfile.write("Ripping file: " + filename + " at " + time.asctime() + "\n")

try:
    while time.time() - starttime < riplength:
        # attempt to rip for the specified length of time
        try:
            # read the specified number of bytes from the stream
            # write those bytes to the output file
            outputfile.write(bytestream.read(2000))  #20000 bytes = 1 sec of recording @ 160kbps
            # test different values for the parameter of read()
            # 10000 - worked for nearly a year
            # 5000 - still skippy.  lost nearly 40 minutes out of 3 hours.
            # 2000?
            # 20000?
        except IOError as (errno, strerror):
            #read() throws an IO error if connection fails
            #any kind of IO error gets handled here
            #error messages are written to the log file
            #while loop continues
            logfile.write("   IOError at " + time.asctime() + "\n")
        except:
            #any other kind of exception gets handled here
            #while loop breaks and program crashes
            #error message is written to log file        
            logfile.write("   Unexpected error at " + time.asctime() + "\n")
            logfile.write("*" * 50 + "\n")
            logfile.write(traceback.print_exc())
            #might be possible to salvage the MP3 at this point, and write it to the podcast???
            raise
finally:
    #always closes the output file before crashing
    outputfile.close()
    logfile.write("Ripping stopped at " + time.asctime() + "\n")
    
# copy the raw rip for analysis
# raw file seems to sound fine.  5/3/2011
# processed stream is garbled
shutil.copy(tempname, outputfolder + "rawbytes.mp3")



#file is finished ripping and has been saved locally. Next, process the raw data
#  1. strip all bytes before the first valid MP3 header
#  2. strip all bytes after the last valid MP3 frame
#  3. strip out any invalid bytes between the first and last valid headers 
#  4. add Xing header to beginning of stream
#  5. save the processed file


logfile.write("Starting to process raw MP3 file\n")

logfile.write("Reading MP3 file\n")
inputfile = open(tempname, 'rb') #open the temporary file in binary read mode
instream = inputfile.read()      #read the contents of the temp file
inputfile.close()

logfile.write("MP3 file read, creating new output file\n")


# Attempt to process the saved MP3 file into a properly formatted MP3
#reopen local file to rewrite processed bitstream
#outputfile = open(tempname, 'wb')

#try:
    #get the data about the MP3 stream
    #save the valid frames to the output file
#    filedata = myMP3.ParseFrames(instream, outputfile)
#finally:
    # if successful, the output file will have all invalid frames removed
    # otherwise, close the outputfile before crashing
#    outputfile.close()


# logfile.write("MP3 file parsed\n")

#frames = filedata[0]
#invalidFrames = filedata[1]
#totalbytes = filedata[2]
#finalbyte = filedata[3]
#toc = filedata[4]
#
#logfile.write("Valid Frames   : " + str(frames) + "\n")
#logfile.write("Invalid Frames : " + str(invalidFrames) + "\n")
#logfile.write("Invalid / Valid: %f\n" % (invalidFrames/frames))

#get Xing header


#Xing = myMP3.MakeXing(frames, finalbyte, toc)

#logfile.write("Xing header created\n")



#Note: the number of frames returned from the MakeXing function will include the final
#      frame, which will almost certainly be truncated. But, the value will be correct
#      when the frame containing the Xing header is added.
#      Also, the number of bytes will include the leading and trailing bytes, which will
#      be chopped off in the final file. This value should not be used in the Xing header

#opening final file for output

logfile.write("Writing final output file\n")

finalfile = open(fullname, 'wb') #open the new output file in binary write mode


#finalfile.write(Xing) #write the Xing header to the output file

# re-read the processed version of the temporary MP3 file
inputfile = open(tempname, 'rb') #reopen the temporary file in binary read mode
instream = inputfile.read()      #reread the contents of the temp file
inputfile.close()

finalfile.write(instream)
#write the MP3 data from the start of first valid frame to the end of last valid frame.

finalfile.close()

logfile.write("Final MP3 file stored, updating RSS feed\n")


#MP3 file has been processed, Xing header added, update the RSS feed


# ***** Consider making this a separate module *****

#format the new item entry

itemtitle = time.strftime("%B %d, %Y - %A")               #'July 03, 2007 - Tuesday'
itemurl = httppath + filename + ".mp3"                    #URL of MP3 file on http server

# get today's program information from the KCRW website
programdesc = MBEscraper.getShowInfo()

# add ID3 tags to the MP3 file

# Podcast naming conventions
# TPE1 - Artist name "The Nerdist", "TWiT", or the hosts, etc.
# TIT2 - Title of individual episode
# TALB - Title of podcast: "Triangulation", "This Week in Tech", etc
# genre: podcast
# media kind: podcast
# description:  show notes
# year

ID3tag = MP3(fullname)
ID3tag["TPE1"] = TPE1(encoding=3, text=["KCRW"])
ID3tag["TIT2"] = TIT2(encoding=3, text=[itemtitle])
ID3tag["TALB"] = TALB(encoding=3, text=["Morning Becomes Eclectic"])
ID3tag["TYER"] = TYER(encoding=3, text=["2012"])
ID3tag["TCON"] = TCON(encoding=3, text=["Podcast"])
ID3tag.save()


# get the final length of the MP3 file
itemlength = getsize(fullname)                            #size of file in bytes

newitem = '''

      <item>
        <title>%s</title>
        <enclosure
          url="%s"
          length="%i"
          type="audio/mpeg" />
        <description>%s</description>
        <pubDate>%s</pubDate>
      </item>''' % (itemtitle, itemurl, itemlength, programdesc, pubDate)

#  open RSS file, locate point of insertion, insert new item, save rewritten RSS file

RSS = open(rssfeed, 'r')
RSSinput = RSS.readlines()
RSS.close()

#store new output text
RSSoutput = ""

for line in RSSinput:

    if line[:13] == "    <pubDate>":
        #update the pubDate tag in the Channel element
        RSSoutput = RSSoutput + "    <pubDate>%s</pubDate>\n" % (pubDate)
    elif "<!-- INSERTION POINT -->" in line:
        #insert the new item here
        RSSoutput = RSSoutput + line + newitem
    else:
        RSSoutput = RSSoutput + line

#save the new XML file by writing over the previous file
newRSS = open(rssfeed, 'w')
newRSS.write(RSSoutput)
newRSS.close()

logfile.write("XML file updated.\n")
logfile.write("Operation complete at " + time.asctime() + "\n\n\n")

#close the log file and restore stderr
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
logfile.close()


#delete the MP3 from the http directory
#delete the file from the "Incomplete" directory

#done

