import unittest
import re

def parseInput(input):
    numbers = [int(s) for s in re.findall(r'\d+', input)]
    count = round(len(numbers) / 2)
    return [(numbers[i], numbers[i + count]) for i in range(0, count)]

def solveRace(time, dist):
    first = next(h for h in range(1, time) if h * (time - h) > dist)
    last = next(h for h in reversed(range(1, time)) if h * (time - h) > dist)

    return last - first + 1

def parse1(input):
    data = parseInput(input)
    result = 1

    for time, dist in data:
        result *= solveRace(time, dist)

    return result

def mergeNumbers(data):
    time = ''
    distance = ''
    for (t, d) in data:
        time += str(t)
        distance += str(d)

    return (int(time), int(distance))

def parse2(input):
    time, dist = mergeNumbers(parseInput(input))
    return solveRace(time, dist)

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""Time:      7  15   30
Distance:  9  40  200"""), 288)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""Time:      7  15   30
Distance:  9  40  200"""), 71503)

unittest.main(exit=False)

with open('input6.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

