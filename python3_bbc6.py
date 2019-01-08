import urllib.request

bbc6 = r'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p'
ripfile = open(r'C:\test\bbc6.mp3', 'wb')
bytestream = urllib.request.urlopen(bbc6)

ripfile.write(bytestream.read(1000000)) # read 1 MB from the stream

ripfile.close()
bytestream.close()

print('done')
