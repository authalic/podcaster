

from datetime import date
# class representing a podcast Episode

# an Episode represents a single day's recording and metadata
# Episode objects are created and managed by Podcast objects

xmlfile = r'http://192.168.1.198/podcast/MBE.xml'  # url of podcast feed
# the xml feed URL will be managed by the Podcast object


class Episode():
    self.title = ''
    self.summary = ''  # episode summary
    self.url = ''  # url of mp3 file accessible from http
    self.localpath = ''  # location of MP3 file stored on server
    self.pubDate = date.today()  # date of recording
    self.length = 0  # length of file in bytes
    self.tracklist = '' # contains a list of tracks in episode, if available from server

    def set_title(self, title):
        self.title = title

    def deleteMP3(self):
        pass # delete the MP3 from the server and remove its entry from the XML file
