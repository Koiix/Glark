from torrent import Torrent
from tracker import Tracker, TrackerResponse

t = Torrent('../ubuntu-18.04.3-desktop-amd64.iso.torrent')
track = Tracker(t)
resp = track.request(0,0,'started')
print(resp)
