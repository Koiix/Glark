# Used to store information needed for a request to the tracker

class TrackerRequest:
    def __init__(self, info_hash, peer_id, ip, port, uploaded, downloaded, left, event):
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.ip = ip
        self.port = p
        self.uploaded = uploaded
        self.downloaded = downloaded
        self.left = left
        self.event = event
