#Class used to handle the Bencoding for torrent files
from collections import OrderedDict


class Parser:

    # Indicates start of integers
    TOKEN_INT = b'i'

    # Indicates start of list
    TOKEN_LIST = b'l'

    # Indicates start of dict
    TOKEN_DICT = b'd'

    # Indicate end of lists, dicts and integer values
    TOKEN_END = b'e'

    # Delimits string length from string data
    TOKEN_STR = b':'

    # encodes generic data or data structure according to BE standards
    #
    # acceptable data types for data include string, integer, list, dictionary, ordered dictionary, and bytes/bytearray
    # returns bytes object
    @staticmethod
    def encode(data) -> bytes:
        if type(data) == str:
            return Parser.encode_str(data)
        elif type(data) == int:
            return Parser.encode_int(data)
        elif type(data) == list:
            return Parser.encode_list(data)
        elif type(data) == dict or type(data) == OrderedDict:
            return Parser.encode_dict(data)
        # if for some reason, bytes are to be encoded, we will basically treat them like strings, without encoding the value
        elif type(data) == bytes:
            return Parser.encode_bytes(data)

    @staticmethod
    def encode_str(val: str) -> bytes:
        # str.encode used to do UTF-8 encoding required by specifications
        return str(len(val) + ":" + val).encode('UTF-8')

    @staticmethod
    def encode_int(val: int) -> bytes:
        # str.encode used to do UTF-8 encoding required by specifications
        return ("i" + str(val) + "e").encode('UTF-8')

    @staticmethod
    def encode_list(val: list) -> bytes:
        result = bytearray('l', 'UTF-8')
        for i in val:
            result += Parser.encode(i)
        return result + Parser.TOKEN_END

    @staticmethod
    def encode_dict(val: dict) -> bytes:
        result = bytearray('d', 'UTF-8')
        for k, v in val.items():
            result += Parser.encode(k)
            result += Parser.encode(v)
        return result + Parser.TOKEN_END

    @staticmethod
    def encode_bytes(val: bytes) -> bytes:
        result = bytearray()
        result += str(len(val)).encode('UTF-8')
        result += Parser.TOKEN_STR
        return result + val

    # decodes bytes provided by Bencoding standards into data/data structure the bytes represent
    # returns a string, integer, list, dictionary, and/or ordered dictionary
    @staticmethod
    def decode(data: bytes):
        # This first byte will always be important, rather a token specifying the beginning of a list, dict, etc
        b = data[0]
        if b is None:
            pass
            # TODO what to do if unexpected EOF?
        #
        data = data[1:len(data)]
        options = {
            Parser.TOKEN_INT: Parser.decode_int,
            Parser.TOKEN_STR: Parser.decode_str,
            Parser.TOKEN_LIST: Parser.decode_list,
            Parser.TOKEN_DICT: Parser.decode_dict,
        }
        if(options[b]!=None):
            return options[b](data)

    def decode_dict(data: bytes):
        d = {}
        while data[0] != Parser.TOKEN_END:
            key = Parser.decode_str(data)
            data = data[len(key):len(data)]
            val = Parser.decode(data)
            data = data[len(val):len(data)]
        data=data[1:len(data)]
        return d
    def decode_list(data: bytes):
        l = []
        while data[0] != Parser.TOKEN_END:
            item = Parser.decode(data)
        return
    def decode_str(data: bytes):
        return
    def decode_int(data: bytes):
        return
