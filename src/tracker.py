# Used to store information needed for tracker request/response and state
import random
import asyncio
import aiohttp
import socket
from torrent import Torrent
from collections import namedTuple

REGISTERED_PORTS = [6881+i for i in range(0,9)]

## TODO complete this named tuple and create function in Tracker to construct it
class Response:

    Peer = namedtuple('Peer', 'id ip port')

    def __init__(self, data: dict):
        self.data = data

    @property
    def failure(self):
        #Optional
        if 'failure reason' in self.data:
            return self.data['failure reason']
        return None

    @property
    def warning(self):
        #Optional
        if 'warning message' in self.data:
            return self.data['warning message']
        return None

    @property
    def interval(self):
        return self.data['interval']

    @property
    def min_interval(self):
        #Optional
        if 'min interval' in self.data:
            return self.data['min interval']
        return None

    @property
    def tracker_id(self):
        return self.data['tracker id']

    @property
    def complete(self):
        return self.data['complete']

    @property
    def incomplete(self):
        return self.data['incomplete']

    # processing of peers attribute done here
    # returns list of Peer tuples declared above
    @property
    def peers(self):
        peers_data = self.data['peers']
        peers_list = []
        if type(peers_data) == list:
            for d in peers_data:
                peers_list.append(Peer(d['peer id'], d['ip'], d['port']))
            return peers_list
        elif type(peers_data) == str:
            peers_list = [peers_data[i:i+6] for i in range(0, len(peers_data), 6)]
            return [Peer(i, p[0:4], p[4:]) for p in peers_list]
        else:
            return None


class Tracker:

    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = _gen_peer_id()
        self.http_handler = aiohttp.ClientSession()
        self.port = _gen_port()

    async def _fetch(handler, url):
        async with handler.get(url) as response:
            return await response

    async def close(self):
        await self.http_client.close()

    async def request(self, uploaded, downloaded, state=None) -> TrackerResponse:

        ## TODO: optional request params i.e. 'numwant','key','trackerid'

        ## Forge HTTP GET Request for tracker
        params = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': self.port,
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': self.torrent.size - downloaded
        }


        if state is not None:
            ## TODO: validate state?
            params['event'] = state

        req_url = self.torrent.announce + "?" + urlencode(params)

        async with self.http_handler as handler:
            http_response = await fetch(handler, req_url)
            if not http_response.status == 200:
                pass
                ## TODO error handling
            encoded = await http_response.read()
            self.last_response = Response(Parser.decode(encoded))
            return self.last_response

    def _gen_peer_id():
        peer_id = '-GT0001-'
        for i in range(1, 12):
            peer_id += str(random.randint(0,9))
        return peer_id

    def _gen_port():
        for port in REGISTERED_PORTS:
            # check port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) == 0:
                    return port

        ## TODO: raise error
        return None
