# Used to store information needed for tracker request/response and state
import random
import aiohttp
import asyncio
import socket
from torrent import Torrent
from collections import namedTuple

## TODO complete this named tuple and create function in Tracker to construct it
Response = namedTuple('Response', )

REGISTERED_PORTS = [6881+i for i in range(0,9)]

class Response:

    def __init__(self, response: dict):
        ## TODO: init .. xd

class Tracker:

    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = _gen_peer_id()
        self.http_handler = aiohttp.ClientSession()
        self.port = _gen_port()
        self.first = True

    async def _fetch(handler, url):
        async with handler.get(url) as response:
            return await.response

    async def request(self, uploaded=None, downloaded=None) -> TrackerResponse:
        # if optional arguments not provided, use state stored with Tracker as default
        if uploaded is None:
            uploaded = self.uploaded
        if downloaded is None:
            downloaded = self.downloaded

        ## Forge HTTP GET Request for tracker
        ## TODO: optional request params i.e. 'numwant','key','trackerid'
        params = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': self.port,
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': self.torrent.size - downloaded
        }



        if self.first:
            params['event'] = 'started'
            first = False
        ## TODO: implement events 'stopped' and 'completed'

        req_url = self.torrent.announce + "?" + urlencode(params)

        async with self.http_handler as handler:
            http_response = await fetch(handler, req_url)
            if not http_response == 200:
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
