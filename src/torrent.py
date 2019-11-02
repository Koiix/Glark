from bencoding import Parser
from hashlib import sha1
from collections import namedTuple

    class Torrent:

    TFile = namedTuple('TorrentFile', ['name','path','length'])

        def __init__(self, filepath):

            self.files = []

            with open(filepath, 'rb') as f:
                meta_data = Parser.decode(f.read())
                self.info = meta_data[b'info']
                self.announce = meta_data[b'announce']

            if self.multi_file:
                for f in self.info[b'files']:
                    name_offset = len(f[b'path']) - 1
                    if name_offset == 0:
                        # TODO Raise error
                    self.files.append(
                    TFile(f[b'path'][name_offset].decode('utf-8'), f[b'path'], f[b'length'])
                    )
            else:
                self.files.append(
                TFile(self.info[b'name'].decode('utf-8'), None, self.info[b'length'])
                )

        @property
        def info_hash(self):
            encoded = Parser.encode(self.info)
            self.info_hash = sha1(encoded).digest()

        @property
        def files(self):
                return self.files

        @property
        def multi_file(self):

            # b'files' -> multi , b'length' -> single
            return b'files' in self.info and not b'length' in self.info

        @property
        def announce(self):
            return self.announce.decode('utf-8')

        @property
        def piece_length(self):
            return self.info[b'piece length']

        @property
        def md5sum(self):
            if b'md5sum' in self.info:
                return self.info[b'md5sum']
            return None

        @property
        def size(self):
            sum_bytes = 0
            for f in self.files:
                sum_bytes += f.length
            return sum_bytes

        @property
        def pieces(self):
            data = self.info[b'pieces']
            pieces = []
            offset = 0

            while offset < len(data):
                pieces.append(data[offset:offset + 20])
                offset += 20
            return pieces
