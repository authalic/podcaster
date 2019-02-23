
import requests
import time
from datetime import datetime
from datetime import timedelta


bbc6 = r'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p'
filename = r'/Users/justin/Projects/Python/podcaster/bbc6_runtest.mp3'

r = requests.get(bbc6, stream=True)

duration = 3 # (hours)

cnt = 0

with open(filename, 'wb') as fd:
    t = datetime.now()

    try:

        for chunk in r.iter_content(chunk_size=256):
            if ((datetime.now() - t) < timedelta(hours=duration)):
                fd.write(chunk)
                cnt = cnt + 1
                if cnt%100 == 0:
                    print(time.strftime("%H:%M:%S", time.localtime()))

            else:
                break

    except Exception as e:

        print(type(e))
        print(e.args)
        print(e)

        print("\nruntime: " + str(datetime.now() - t))

print("\ndone")
