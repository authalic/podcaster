
import requests
import time
from datetime import datetime
from datetime import timedelta
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout


bbc6 = r'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p'
filename = r'/Users/justin/Projects/Python/podcaster/bbc6_runtest.mp3'

r = requests.get(bbc6, stream=True, timeout=(30, 12)) # timeout(connect, read)

duration = 3 # (hours)

stoptime = datetime.now() + timedelta(hours=duration)


def ripstream(append=False):

    cntr = 0  # for testing purposes, to demo that the program is still running
    if append:
        # an error has occurred to get to this point
        # restart the streaming and append the new data to the previously stopped data file

        print("appending to existing file\n")
        streamstore = open(filename, 'ab')
    else:
        # streaming begins here
        # output is written to a new and empty file

        print("streaming to new file\n")
        streamstore = open(filename, 'wb')

    with streamstore as fd:

        print("stop time: ", stoptime)
        print("streaming...\n")

        try:
            for chunk in r.iter_content(chunk_size=256):
                if (datetime.now() < stoptime):
                    fd.write(chunk)
                    cntr = cntr + 1

                    if cntr > 1600:
                        print(time.strftime("%H:%M:%S", time.localtime()))
                        cntr = 0

                else:
                    break

        except ConnectionError as e:
            print("Requests Connection Error\n")
            print(type(e))
            print(e.args)
            print(e)
            print("\nAttempting to restart stream\n")

            ripstream(append=True)

        except (ConnectTimeout, ReadTimeout) as e:
            print("Requests Timeout Error")
            print(type(e))
            print(e.args)
            print(e)

ripstream()

print("\ndone")
