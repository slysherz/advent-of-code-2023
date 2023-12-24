import unittest
import re
import itertools

def parseInput(input, repeats):
    result = []

    for line in input.splitlines():
        springs, ns = line.split(' ')
        result.append((springs * repeats, [int(n) for n in ns.split(',')] * repeats))

    return result

def countGroups(line):
    return [len(s) for s in re.findall(r'#+', line)]

def solveGroup(string, count):
    if len(string) < len(count) - 1 + sum(count): return 0

    

def solveLine(string, count):
    


def parse1(input):
    data = parseInput(input)
    result = 0
    for line, ns in data:
        result += solveLine(line, ns)
    return result

def parse2(input):
    data = parseInput(input)
    return 0

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""), 21)
        
    
    def test_part2(self):
        self.assertEqual(parse2(""" """), 0)

unittest.main(exit=False)

with open('input12.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

