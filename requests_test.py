
import requests

# get the current track
# r = requests.get(r'http://tracklist-api.kcrw.com/Simulcast')


# get the tracklist from a date
tracklist = requests.get(r'https://tracklist-api.kcrw.com/Simulcast/date/2018/05/15').json()

for track in tracklist:
    if track['program_start'] == "09:00":
        if "BREAK" in track['artist']:
            print(track['time'] + "  - BREAK -")
        else:
            print(track['time'] + "  " + track['artist'] + " - " + track['title'] )
