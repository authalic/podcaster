import requests

kcrw = r'http://kcrw.streamguys1.com/kcrw_192k_mp3_on_air'

filename = r'test.mp3'


r = requests.get(kcrw, stream=True)

with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

