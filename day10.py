import unittest
import re

N = (0, -1)
S = (0, 1)
W = (-1, 0)
E = (1, 0)
PIPES = {
    '|': [N, S],
    '-': [W, E],
    'L': [N, E],
    'J': [N, W],
    '7': [W, S],
    'F': [S, E],
    '.': [],
    'S': []
}

def parseInput1(input):
    map = [line for line in input.splitlines()]
    height = len(map)
    width = len(map[0])

    return (map, width, height)

def valid(pos, width, height):
    x, y = pos
    return x >= 0 and x < width and y >= 0 and y < height

def generateMap(context):
    map, width, height = context
    graph = {}
    for y in range(0, height):
        for x in range(0, width):
            graph[(x, y)] = []

    start = None
    for y in range(0, height):
        for x in range(0, width):
            pipe = map[y][x]
            if pipe == 'S': start = (x, y)
            for (dx, dy) in PIPES[pipe]:
                pos = (x + dx, y + dy)
                if valid(pos, width, height):
                    graph[(x, y)].append(pos)

    # Find out the starting pipe
    x, y = start
    for pipe in PIPES:
        failed = False
        for dx, dy in PIPES[pipe]:
            pos = (x + dx, y + dy)
            if (not valid(pos, width, height)) or not ((x, y) in graph[pos]):
                failed = True

        if not failed:
            map[y] = map[y].replace('S', pipe)
            for dx, dy in PIPES[pipe]:
                graph[(x, y)].append((x + dx, y + dy))

    return (graph, start)

def solve1(graph, start):
    rounds = 0
    neighbours = [start]
    visited = {}

    while len(neighbours) > 0:
        next = []
        for pos in neighbours:
            if pos in visited:
                continue
            visited[pos] = True
            for n in graph[pos]:
                if pos in graph[n] and not n in visited:
                    next.append(n)
        
        rounds += 1
        neighbours = next

    return (rounds - 1, visited)

def parse1(input):
    ctx = parseInput1(input)
    graph, start = generateMap(ctx)
    return solve1(graph, start)[0]

def printVisited(visited, width, height):
    result = ''
    for y in range(0, height):
        for x in range(0, width):
            if (x, y) in visited:
                result += '█'
            else:
                result += '-'
        result += '\n'

    print(result)

def countIntersections(cells):
    last_pipe = '.'
    result = 0
    for c in cells:
        if c == '|' or (
            last_pipe == 'F' and c == 'J'
        ) or (
            last_pipe == 'L' and c == '7'
        ): result += 1
        if not c in ['.', '-']: last_pipe = c
    
    return result

def parse2(input):
    map, width, height = parseInput1(input)
    graph, start = generateMap((map, width, height))
    visited = solve1(graph, start)[1]
    printVisited(visited, width, height)

    result = 0
    for y in range(0, height):
        for x in range(0, width):
            if (x, y) in visited: continue
            cells = ''.join(c if (i, y) in visited else '.' for i, c in enumerate(map[y][0:x]))
            if countIntersections(cells) % 2 == 1:
                result += 1

    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""), 8)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""), 4)
        
    def test_part3(self):
        self.assertEqual(parse2(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""), 8)
        
    def test_part4(self):
        self.assertEqual(parse2("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""), 10)

unittest.main(exit=False)

with open('input10.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

