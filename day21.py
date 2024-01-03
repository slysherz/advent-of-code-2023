import unittest
import heapq

def parseInput(input):
    return [line for line in input.splitlines()]

DIR = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def parse1(input, steps):
    data = parseInput(input)

    start = None
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)
    
    reacheable = [start]
    for i in range(0, steps):
        new_reacheable = []
        for pos in reacheable:
            for dir in DIR:
                new_pos = add(pos, dir)
                x, y = new_pos
                # Skip out of bounds
                if x < 0 or x >= len(data[0]): continue
                if y < 0 or y >= len(data): continue
                # No rocks
                if data[y][x] == '#': continue
                # No repeats
                if new_pos in new_reacheable: continue
                new_reacheable.append(new_pos)
        reacheable = new_reacheable

    return len(reacheable)

def parse2(input):
    data = parseInput(input)
    return 0

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 6), 16)
        
    
    def test_part2(self):
        self.assertEqual(parse2(""" """), 0)

unittest.main(exit=False)

with open('input21.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data, 64))
    print("Part 2:", parse2(data))

