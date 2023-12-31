import unittest

def parseInput(input):
    return [[int(c) for c in line] for line in input.splitlines()]

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def eq(a, b):
    return a[0] == b[0] and a[1] == b[1]

def get(data, pos):
    return data[pos[1]][pos[0]]

def dist(a, b):
    diff = sub(a, b)
    return abs(diff[0]) + abs(diff[1])

DIR = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

def printPath(data, path):
    table = ''
    for y, line in enumerate(data):
        for x, d in enumerate(line):
            if (x, y) in path:
                table += '#'
            else:
                table += str(d)
        table += '\n'
    print(table)

def setCache(cache, node, score):
    path, heat_left = node
    key = tuple(path[-4:])
    cache[key] = (heat_left, score)
    return cache[key]
    
def getCache(cache, node):
    path, heat_left = node
    key = tuple(path[-4:])
    if key in cache:
        hl, val = cache[key]
        if hl >= heat_left:
            return (hl, val)
    return None

def solveNode(data, cache, goal, node):
    path, heat_left = node
    if path[-1] == goal:
        return ('ok', setCache(cache, node, get(data, path[-1])))
    if heat_left < 0:
        return ('ok', setCache(cache, node, None))

    # Check if we solved this case before
    cached = getCache(cache, node)
    if cached != None: return ('ok', cached)

    # Count how many times we went in a straight line
    diff = [sub(path[i], path[i - 1]) for i in range(max(1, len(path) - 3), len(path))]
    forbidden = None
    if len(diff) == 3 and all(p == diff[0] for p in diff):
        forbidden = diff[0]

    pos = path[-1]
    best = None
    heat = get(data, pos)

    # Find all possible next positions, ignoring fobidden ones
    # Try them all, return the best
    tries = []
    for dir in DIR:
        # Can't repeat direction more than 3 times
        if dir == forbidden:
            continue
        # Can't turn back
        if len(diff) > 0 and eq(add(diff[-1], dir), (0, 0)):
            continue
        next = add(pos, dir)
        # Skip if outside the grid
        if next[0] < 0 or next[0] >= len(data[0]) or next[1] < 0 or next[1] >= len(data):
            continue
        if next in path:
            continue
        tries.append(next)

    # Try moving in the direction of the goal first
    tries.sort(reverse=True, key=lambda n: dist(n, goal))

    best = None
    retry = []
    for next in tries:
        next_path = path.copy()
        next_path.append(next)
        next_node = (next_path, heat_left - heat)
        next_cache = getCache(cache, next_node)
        if next_cache == None:
            retry.append(next_node)
            continue

        # We already computed next node, use it
        next_heat, next_value = next_cache
        if next_value == None: continue
        if best == None or best > next_value + heat:
            best = next_value + heat

    if len(retry) > 0:
        return ('retry', retry)
    return ('ok', setCache(cache, node, best))

def solve(data, start, goal):
    cache = {}
    max_score = sum(sum(row) for row in data)
    for i in range(1, max_score, 10):
        print(i)
        start_node = ([start], i)
        stack = [start_node]

        while len(stack):
            res, val = solveNode(data, cache, goal, stack[-1])
            if res == 'ok':
                stack.pop()
            if res == 'retry':
                for v in val: stack.append(v)

        res = getCache(cache, start_node)
        if res[1] != None:
            return res[1]

def parse1(input):
    data = parseInput(input)
    end = (len(data[0]) - 1, len(data) - 1)
    result = solve(data, (0, 0), end)
    return result - get(data, (0, 0))

def parse2(input):
    data = parseInput(input)
    return 0

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""), 102)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""), 0)

unittest.main(exit=False)

with open('input17.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

