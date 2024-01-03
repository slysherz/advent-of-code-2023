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

    width = len(data[0])
    height = len(data)
    
    layers = 6
    total = [0, 0]
    visited_even = [set() for i in range(layers)]
    visited_odd = [set() for i in range(layers)]
    visited_odd[0].add(start)

    for i in range(0, steps):
        if i % 2 == 0:
            visited = visited_even
            reacheable = visited_odd[0]
        else:
            visited = visited_odd
            reacheable = visited_even[0]

        visited.insert(0, set())
        for pos in reacheable:
            for dir in DIR:
                new_pos = add(pos, dir)
                x, y = new_pos
                # No rocks
                if data[y % height][x % width] == '#': continue
                if any((new_pos in layer) for layer in visited):
                    continue
                visited[0].add(new_pos)

        retired = visited.pop()
        total[i % 2] += len(retired)

    if steps % 2 == 1:
        return sum(len(v) for v in visited_even) + total[0]
    else:
        return sum(len(v) for v in visited_odd) + total[1]

def parse2(input):
    # 26501365 = 202300 * 131 + 65
    y0 = parse1(input, 65)
    y1 = parse1(input, 196)
    y2 = parse1(input, 327)
    # n489 = parse1(input, 489)

    c = y0
    a = (y2 - 2 * y1 + c) // 2
    b = y1 - a - c
    
    x = 202300
    y = a * (x * x) + b * x + c
    return y

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

unittest.main(exit=False)

with open('input21.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data, 64))
    print("Part 2:", parse2(data))

