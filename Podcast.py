# Podcast object

# a Podcast object contains Episode objects
# the Podcast knows information about the podcast and knows:
#  - how to create a new Episode object by recording the MP3 and compiling metadata
#  - the URL on the web where the podcast stream is served/broadcast
#  - the scheduling of the broadcasts to record
#  - the path of the XML file on the server
#  - the path of the MP3 file in the server
#  - the URL of the hosted MP3 file on the web server
#  - how to extract data from the XML file
#    - the number of episodes currently in the XML feed and on the server
#    - each episode's date, size, title, etc.
#  - how to test if an episode is beyond its expiration date
#    - delete any episodes beyond this date range

# making system calls in python 3
# https://docs.python.org/3/library/subprocess.html


import subprocess  # for executing file management in the server's file system
from . import Episode


class Podcast:

    def __init__(self):
        self.data = []

    def deleteEpisode(self):
        '''Remove a podcast from the server:
        delete its file from the web server and its entry in the XML feed'''
        pass
