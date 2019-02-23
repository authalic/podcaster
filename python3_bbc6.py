import urllib.request

bbc6 = r'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p'
ripfile = open(r'/Users/justin/Projects/bbc6.mp3', 'wb')
bytestream = urllib.request.urlopen(bbc6)

mbcount = 0

while True:
    ripfile.write(bytestream.read(1000000)) # read 1 MB from the stream
    print('MB: ' + str(mbcount))
    mbcount = mbcount + 1

ripfile.close()
bytestream.close()

print('done')
