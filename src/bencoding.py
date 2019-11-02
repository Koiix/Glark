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
        return (str(len(val)) + ":" + val).encode('UTF-8')

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
        val, parsed = Parser.decode_data(data)
        return val

    @staticmethod
    def decode_data(data: bytes):
        b = data[0:1]
        if b is None:
            return (None, None)
            # TODO what to do if unexpected EOF?

        newdata = data[1:len(data)]

        options = {
            Parser.TOKEN_INT: Parser.decode_int,
            Parser.TOKEN_LIST: Parser.decode_list,
            Parser.TOKEN_DICT: Parser.decode_dict,
            Parser.TOKEN_END: lambda a: (None, 0)
        }
        if b in options:
            val, parsed = options[b](newdata)
            return (val, parsed+1)
        elif b in b'0123456789':
            val, parsed = Parser.decode_str(data)
            return (val, parsed)
        return (None, 0)

    def decode_dict(data: bytes):
        d = {}
        sum_parsed = 0
        while data[0:1] != Parser.TOKEN_END:

            # parse key
            key, parsed = Parser.decode_str(data)
            data = data[parsed:len(data)]
            sum_parsed += parsed

            #parse val
            val, parsed = Parser.decode_data(data)
            data = data[parsed:len(data)]
            sum_parsed += parsed

            d[key] = val
        # move forward one byte for TOKEN_END
        data=data[1:len(data)]
        return (d, sum_parsed + 1)

    def decode_list(data: bytes):
        l = []
        sum_parsed = 0
        while data[0:1] != Parser.TOKEN_END:
            temp, parsed = Parser.decode_data(data)
            sum_parsed += parsed
            data = data[parsed:len(data)]
            l.append(temp)
        return (l, sum_parsed+1)

    def decode_str(data: bytes):
        find = None
        strlen = 0
        try:
            find = data.index(Parser.TOKEN_STR)
            strlen = int(data[0:find])
        except ValueError:
            raise RuntimeError("Unable to find {0} in \"{1}\"".format(Parser.TOKEN_STR, str(data)))
        return (data[find+1:find+1+strlen], strlen + find+1)

    def decode_int(data: bytes):
        find = None
        try:
            find = data.index(Parser.TOKEN_END)
        except ValueError:
            raise RuntimeError("Unable to find {0} in \"{1}\"".format(Parser.TOKEN_END, str(data)))
        return (int(data[0:find]), find+1)
