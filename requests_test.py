
import requests

# get the current track
# r = requests.get(r'http://tracklist-api.kcrw.com/Simulcast')


# get the tracklist from a date
tracklist = requests.get(r'https://tracklist-api.kcrw.com/Simulcast/date/2018/05/15').json()

playlist = ""

for track in tracklist:
    if track['program_start'] == "09:00":
        if "BREAK" in track['artist']:
            playlist += track['time'] + "  - BREAK -" + "\n"
        elif track['label'] == "KCRW Live":
            playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + " [Live @ KCRW]\n"
        else:
            playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + "\n"

print(playlist)