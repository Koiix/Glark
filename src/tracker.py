# Used to store information needed for tracker request/response and state
import random
import aiohttp
import asyncio
from torrent import Torrent

class Tracker:

    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = _gen_peer_id()
        self.http_handler = aiohttp.ClientSession()

    async def _fetch(handler, url):
        async with handler.get(url) as response:
            return await.response

    async def connect(self):
        async with self.http_handler as handler:
            response = await fetch(handler, self.torrent.announce)

    def _gen_peer_id():
        peer_id = '-GT0001-'
        for i in xrange(12):
            peer_id += str(random.randint(0,9))
        return peer_id

class TrackerResponse:

    def __init__(self, response: dict):
        ## TODO: init .. xd
        pass 
