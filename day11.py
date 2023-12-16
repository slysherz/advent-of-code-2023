import unittest

def distance(pos1, pos2, empty_x, empty_y, weight):
    x1, y1 = pos1
    x2, y2 = pos2

    exp_x = len([0 for n in empty_x if min(x1, x2) < n and n < max(x1, x2)])
    exp_y = len([0 for n in empty_y if min(y1, y2) < n and n < max(y1, y2)])

    dist = max(x1, x2) - min(x1, x2) + max(y1, y2) - min(y1, y2) + (exp_x + exp_y) * (weight - 1)
    return dist

def parseInput(input):
    map = [line for line in input.splitlines()]

    empty_y = []
    for y, line in enumerate(map):
        if all(c == '.' for c in line):
            empty_y.append(y)
    
    empty_x = []
    for x in range(0, len(map[0])):
        if all(map[i][x] == '.' for i in range(0, len(map))):
            empty_x.append(x)

    galaxies = []
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x, y))

    return galaxies, empty_x, empty_y


def parse(input, weight):
    coordinates, empty_x, empty_y = parseInput(input)

    result = 0
    for i, a in enumerate(coordinates):
        for b in coordinates[i + 1:]:
            result += distance(a, b, empty_x, empty_y, weight)

    return result

test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse(test, 2), 374)
        
    def test_part2(self):
        self.assertEqual(parse(test, 10), 1030)

    def test_part3(self):
        self.assertEqual(parse(test, 100), 8410)

unittest.main(exit=False)

with open('input11.txt') as file:
    data = file.read()
    print("Part 1:", parse(data, 2))
    print("Part 2:", parse(data, 1000000))

