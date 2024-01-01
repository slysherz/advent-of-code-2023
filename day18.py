import unittest
import re

def parseInput1(input):
    result = []
    for line in input.splitlines():
        m = re.match(r'(\w) (\d+)', line)
        result.append((m[1], int(m[2])))
    return result

DIR = ['R', 'D', 'L', 'U']

def parseInput2(input):
    result = []
    for line in input.splitlines():
        m = re.match(r'\w \d+ \(#(.{5})(.)\)', line)
        result.append((DIR[int(m[2])], int(m[1], 16)))
    return result

def countInterLeft(pos, lines):
    x, y = pos
    result = 0
    for lx, ly1, ly2 in lines:
        if x > lx and y >= ly1 and y < ly2:
            result += 1
    return result

def hitLine(pos, line):
    a, b = line
    if a[0] == b[0]:
        return pos[0] == a[0] and min(a[1], b[1]) <= pos[1] <= max(a[1], b[1])
    else:
        return pos[1] == a[1] and min(a[0], b[0]) <= pos[0] <= max(a[0], b[0])

def solve(data):
    current = (0, 0)
    max_x = float('-inf')
    max_y = float('-inf')

    result = 0
    for dir, count in data:
        x, y = current
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        if dir == 'D':
            end = (x, y + count)
            result += (x + 1) * count
        if dir == 'U':
            end = (x, y - count)
            result -= x * count
        if dir == 'R':
            end = (x + count, y)
            result += count
        if dir == 'L':
            end = (x - count, y)
        current = end

    result += 1
    return result


def parse1(input):
    data = parseInput1(input)
    return solve(data)

def parse2(input):
    data = parseInput2(input)
    return solve(data)

class Test(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(parse1("""R 2
D 1
D 1
L 2
U 1
U 1"""), 9)

    def test_part1_2(self):
        self.assertEqual(parse1("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""), 62)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""), 952408144115)

unittest.main(exit=False)

with open('input18.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

# 40714