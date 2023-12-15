import unittest
import re

def parseInput(input):
    result = []
    for line in input.splitlines():
        result.append([int(s) for s in re.findall(r'-?\d+', line)])
    return result

def sub_next(numbers):
    result = []
    for i in range(1, len(numbers)):
        result.append(numbers[i] - numbers[i - 1])
    return result

def solve1(numbers):
    if all(n == 0 for n in numbers): return 0
    rest = sub_next(numbers)
    last = solve1(rest)
    return last + numbers[-1]

def parse1(input):
    data = parseInput(input)
    return sum(solve1(ns) for ns in data)

def solve2(numbers):
    if all(n == 0 for n in numbers):
        return 0
    rest = sub_next(numbers)
    last = solve2(rest)
    return numbers[0] - last

def parse2(input):
    data = parseInput(input)
    return sum(solve2(ns) for ns in data)

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""), 114)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""), 2)

unittest.main(exit=False)

with open('input9.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

