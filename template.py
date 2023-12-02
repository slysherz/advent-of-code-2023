import unittest

def parse1(input):
    result = 0
    for line in input.splitlines():
        assert(False)
    return result

def parse2(input):
    result = 0
    for line in input.splitlines():
        assert(False)
    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1(""" """), 0)
        
    
    def test_part2(self):
        self.assertEqual(parse2(""" """), 0)

unittest.main(exit=False)

with open('input.txt') as file:
    data = file.read()
    print(parse1(data))
    print(parse2(data))

