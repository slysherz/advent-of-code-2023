import unittest
import re

def parseInput(input):
    result = []
    for str in re.split(r'\r?\n\r?\n', input):
        lines = re.split(r'\r?\n', str.strip())
        lines_rev = ['' for i in range(0, len(lines[0]))]
        for y in range(0, len(lines)):
            for x in range(0, len(lines_rev)):
                lines_rev[x] += lines[y][x]

        result.append((lines, lines_rev))

    return result

def diff(a, b):
    return sum(1 for i in range(0, len(a)) if a[i] != b[i])

def findReflection(lines, goal):
    for sp in range(1, len(lines)):
        diffs = 0
        for i in range(0, sp):
            mirror = sp + sp - i - 1
            if mirror < len(lines) and lines[i] != lines[mirror]:
                diffs += diff(lines[i], lines[mirror])

        if goal == diffs:
            return sp
        
    return None

def parse(input, goal):
    data = parseInput(input)
    result = 0
    for lines, lines_rev in data:
        res = findReflection(lines, goal)
        if res != None:
            result += 100 * res

        res = findReflection(lines_rev, goal)
        if res != None:
            result += res

    return result

def parse1(input):
    return parse(input, 0)

def parse2(input):
    return parse(input, 1)

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""), 405)
    
    def test_part2(self):
        self.assertEqual(parse2("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""), 400)

unittest.main(exit=False)

with open('input13.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

