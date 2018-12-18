
import requests
from datetime import date

# get the KCRW tracklist for the current date

def get_playlist(starttime = "06:00"):

    t = date.today()
    playlist_url = r'https://tracklist-api.kcrw.com/Simulcast/date/{}/{}/{}'.format(t.year, t.month, t.day) 
    tracklist = requests.get(playlist_url).json()
    playlist = ""

    for track in tracklist:
        if track['program_start'] == starttime:
            if "BREAK" in track['artist']:
                playlist += track['time'] + "  - BREAK -" + "\n"
            elif track['label'] == "KCRW Live":
                playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + " [Live @ KCRW]\n"
            else:
                playlist += track['time'] + "  " + track['artist'] + " - " + track['title'] + "\n"

    return playlist

# call the function for testing

todaylist = get_playlist()
print(todaylist)
