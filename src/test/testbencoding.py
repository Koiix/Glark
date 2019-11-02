import sys
sys.path.insert(0, sys.path[0] + '/..')
import unittest
from bencoding import *

class TestDecoding(unittest.TestCase):

    def test_string(self):
        s = Parser.decode(b'11:Hello World')
        self.assertEqual(s, 'Hello World')

    def test_int(self):
        i = Parser.decode(b'i529e')
        self.assertEqual(i, 529)

    def test_listSimple(self):
        correct = ['doggo', 'logarithm', 'fire', '', 43]
        test = Parser.decode(b'l5:doggo9:logarithm4:fire0:i43ee')
        self.assertEqual(test, correct)

    def test_dictSimple(self):
        correct = {
            'how':'do',
            'I':'write',
            'robust':'tests?',
            'fuck it':'bottom text',
            'joel':47
        }
        test = Parser.decode(b'd3:how2:do1:I5:write6:robust6:tests?7:fuck it11:bottom text4:joeli47ee')
        self.assertEqual(correct, test)

    def test_dictComplex(self):
        correct = {
            'this': 314,
            'dict': {'lol': ['whatthe', 356], 'not':432},
            'sucks': 'weirdchamp'
        }
        test = Parser.decode(b'd4:thisi314e4:dictd3:loll7:whatthei356ee3:noti432ee5:sucks10:weirdchampe')
        self.assertEqual(correct, test)

    def test_listComplex(self):
        correct = ['hello', ['nested', 'list'], 243, {'nested': 'dict', 'dog':732}, 'end', 1]
        test = Parser.decode(b'l5:hellol6:nested4:listei243ed6:nested4:dict3:dogi732ee3:endi1ee')
        self.assertEqual(correct, test)


class TestEncoding(unittest.TestCase):

    def test_string(self):
        test = Parser.encode('brehmisdog')
        correct = b'10:brehmisdog'
        self.assertEqual(correct, test)

    def test_int(self):
        test = Parser.encode(439)
        correct = b'i439e'
        self.assertEqual(correct, test)

    def test_listSimple(self):
        test = Parser.encode([45, 'goodbye', 'my', 'sweet', 'prince', 19])
        correct = b'li45e7:goodbye2:my5:sweet6:princei19ee'
        self.assertEqual(test, correct)

    def test_listComplex(self):
        test = Parser.encode([2, ['how', 'make'], 'dog', {'9':11}])
        correct = b'li2el3:how4:makee3:dogd1:9i11eee'
        self.assertEqual(test, correct)

    def test_dictSimple(self):
        test = Parser.encode({
            'xdnoob': 420,
            'dogwarrior': 'log',
            'wowza': 26
        })
        correct = b'd6:xdnoobi420e10:dogwarrior3:log5:wowzai26ee'
        self.assertEqual(correct, test)

    def test_dictComplex(self):
        test = Parser.encode({
            'dict':{'i1':65, '38':'notnum'},
            'list':[86, 21, 'yeow'],
            'randomval': 543
        })
        correct = b'd4:dictd2:i1i65e2:386:notnume4:listli86ei21e4:yeowe9:randomvali543ee'
        self.assertEqual(correct, test)

if __name__ == '__main__':
    unittest.main()
