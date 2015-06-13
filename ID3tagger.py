

from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TALB, TYER, TCON


filename = 'C:\\test\\banks.mp3'


audio = MP3(filename)

# Podcast naming conventions
# TPE1 - Artist name "The Nerdist", "TWiT", or the hosts, etc.
# TIT2 - Title of individual episode
# TALB - Title of podcast: "Triangulation", "This Week in Tech", etc
# genre: podcast
# media kind: podcast
# description:  show notes
# year



audio["TIT2"] = TIT2(encoding=3, text=["The Base"])
audio["TPE1"] = TPE1(encoding=3, text=["Paul Banks"])
audio["TALB"] = TALB(encoding=3, text=["Banks"])
audio["TYER"] = TYER(encoding=3, text=["2012"])
audio["TCON"] = TCON(encoding=3, text=["Podcast"])
audio.save()


