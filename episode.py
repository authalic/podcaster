

from datetime import date

# class representing a podcast episode

class Episode():
    self.title = ''
    self.summary = ''  # episode summary
    self.url = ''  # url of mp3 file accessible from http
    self.localpath = ''  # location of file stored on server
    self.pubDate = date.today()  # date of recording
    self.length = 0  # length of file in bytes
