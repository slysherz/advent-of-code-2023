import unittest
import heapq

SLOPE = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}
DIR = SLOPE.values()

def parseInput(input):
    return [line for line in input.splitlines()]

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def maxPath(data, start, goal, slope):
    paths = [(0, [start])]
    best = 0

    while len(paths):
        steps, path = heapq.heappop(paths)
        pos = path[-1]
        if pos == goal:
            best = max(best, -steps)
            continue

        for dir in DIR:
            next = add(pos, dir)
            x, y = next
            if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data): continue
            c = data[y][x]
            if c == '#': continue
            if next in path: continue
            npath = path.copy()
            if c in slope:
                nn = add(next, slope[c])
                if nn == pos: continue
                npath.append(nn)
                heapq.heappush(paths, (steps - 2, npath))
            else:
                npath.append(next)
                heapq.heappush(paths, (steps - 1, npath))

    return best

def maxPath2(data, start, goal):
    visited = set()
    nodes = [(start, 0, start)]
    graph = {
        start: []
    }
    while len(nodes):
        parent, dist, pos = nodes.pop()
        def valid(dir):
            next = add(pos, dir)
            x, y = next
            if x < 0 or x >= len(data[0]) or y < 0 or y >= len(data): return False
            c = data[y][x]
            if c == '#': return False
            return True
        
        neighbours = [dir for dir in DIR if valid(dir)]
        if len(neighbours) < 3:
            if pos in visited: continue
            visited.add(pos)
        
        if pos == goal:
            graph[goal] = [(parent, dist)]
            graph[parent].append((goal, dist))
            continue

        if len(neighbours) == 1 and pos != start:
            # Skip dead ends
            continue
        if len(neighbours) == 2 or pos == start:
            for dir in neighbours:
                next = add(pos, dir)
                if not next in visited and parent != next:
                    nodes.append((parent, dist + 1, next))
            continue

        if not pos in graph: graph[pos] = []
        graph[pos].append((parent, dist))
        graph[parent].append((pos, dist))

        for dir in neighbours:
            next = add(pos, dir)
            nodes.append((pos, 1, next))

    paths = [(0, [start])]
    result = 0
    while len(paths):
        dist, path = paths.pop()
        current = path[-1]

        if current == goal:
            result = max(result, dist)
            continue

        for next, w in graph[current]:
            if next in path: continue
            next_path = path.copy()
            next_path.append(next)
            paths.append((w + dist, next_path))

    return result

def parse1(input):
    data = parseInput(input)
    return maxPath(data, (1, 0), (len(data[0]) - 2, len(data) - 1), SLOPE)

def parse2(input):
    data = parseInput(input)
    return maxPath2(data, (1, 0), (len(data[0]) - 2, len(data) - 1))

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""), 94)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""), 154)

unittest.main(exit=False)

with open('input23.txt') as file:
    data = file.read()
    # print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

