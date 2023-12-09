import unittest

def parseInput(input):
    result = 0
    for line in input.splitlines():
        pass
    return result


def parse1(input):
    data = parseInput(input)
    return 0

def parse2(input):
    data = parseInput(input)
    return 0

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1(""" """), 0)
        
    
    def test_part2(self):
        self.assertEqual(parse2(""" """), 0)

unittest.main(exit=False)

with open('input.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

