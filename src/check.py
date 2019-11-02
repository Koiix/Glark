from bencoding import Parser

with open('../static/ubuntu-18.04.3-desktop-amd64.iso.torrent', 'rb') as f:
    meta = f.read()
    d = Parser.decode(meta)
    print(d[b'announce'])
