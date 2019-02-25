
import requests
import time
from datetime import datetime
from datetime import timedelta
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout


bbc6 = r'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p'
filename = r'/Users/justin/Projects/Python/podcaster/bbc6_runtest.mp3'

r = requests.get(bbc6, stream=True, timeout=(3.5, 31)) # timeout(connect, read)

duration = 3 # (hours)

stoptime = datetime.now() + timedelta(hours=duration)

cnt = 0

with open(filename, 'wb') as fd:

    try:
        for chunk in r.iter_content(chunk_size=256):
            if (datetime.now() < stoptime):

                fd.write(chunk)
                cnt = cnt + 1
                if cnt%100 == 0:
                    print(time.strftime("%H:%M:%S", time.localtime()))

            else:
                break

    except (ConnectionError, ConnectTimeout, ReadTimeout) as e:
        print("Requests Error")
        print(type(e))
        print(e.args)
        print(e)

    except Exception as e:
        print("Exception")
        print(type(e))
        print(e.args)
        print(e)

print("\ndone")


'''
<class 'requests.exceptions.ConnectionError'>
(ReadTimeoutError("HTTPConnectionPool(host='bbcmedia.ic.llnwd.net', port=80): Read timed out.",),)
HTTPConnectionPool(host='bbcmedia.ic.llnwd.net', port=80): Read timed out.

<class 'requests.exceptions.ConnectionError'>
(ReadTimeoutError("HTTPConnectionPool(host='bbcmedia.ic.llnwd.net', port=80): Read timed out.",),)
HTTPConnectionPool(host='bbcmedia.ic.llnwd.net', port=80): Read timed out.

'''