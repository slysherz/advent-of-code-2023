import unittest
import heapq

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

def solveNode(data, node, goal, cache):
    curr_heat, pos, dir_in_row, last_dir, path = node
    if pos == goal:
        printPath(data, path)
        return ('done', curr_heat)
    key = (pos, dir_in_row, last_dir)
    if key in cache: return ('next', [])
    else: cache[key] = True
    result = []
    for dir in DIR:
        # Can't repeat direction more than 3 times
        if dir_in_row == 3 and dir == last_dir:
            continue
        # Can't turn back
        if last_dir != None and eq((0, 0), add(dir, last_dir)):
            continue
        next = add(pos, dir)
        # Skip if outside the grid
        if next[0] < 0 or next[0] >= len(data[0]) or next[1] < 0 or next[1] >= len(data):
            continue
        heat = get(data, next)
        new_path = path.copy()
        new_path.append(next)
        same_dir = last_dir == dir
        next_dir_in_row = dir_in_row + 1 if same_dir else 1
        result.append((curr_heat + heat, next, next_dir_in_row, dir, new_path))

    return ('next', result)

def solveNode2(data, node, goal, cache):
    curr_heat, pos, dir_in_row, last_dir, path = node
    if pos == goal:
        if dir_in_row >= 4:
            printPath(data, path)
            return ('done', curr_heat)
        return ('next', [])

    key = (pos, dir_in_row, last_dir)
    if key in cache: return ('next', [])
    else: cache[key] = True
    result = []
    for dir in DIR:
        # Must go straight if changed direction recently
        if last_dir != None and dir_in_row < 4 and last_dir != dir:
            continue
        # Can't repeat direction more than 3 times
        if dir_in_row == 10 and dir == last_dir:
            continue
        # Can't turn back
        if last_dir != None and eq((0, 0), add(dir, last_dir)):
            continue
        next = add(pos, dir)
        # Skip if outside the grid
        if next[0] < 0 or next[0] >= len(data[0]) or next[1] < 0 or next[1] >= len(data):
            continue
        heat = get(data, next)
        new_path = path.copy()
        new_path.append(next)
        same_dir = last_dir == dir
        next_dir_in_row = dir_in_row + 1 if same_dir else 1
        result.append((curr_heat + heat, next, next_dir_in_row, dir, new_path))

    return ('next', result)

def solve(data, start, goal, rules):
    cache = {}
    heap = []
    heapq.heappush(heap, (0, start, 0, None, []))
    while True:
        node = heapq.heappop(heap)
        res, val = rules(data, node, goal, cache)
        if res == 'done':
            return val
        for n in val:
            heapq.heappush(heap, n)

def parse1(input):
    data = parseInput(input)
    end = (len(data[0]) - 1, len(data) - 1)
    result = solve(data, (0, 0), end, solveNode)
    return result

def parse2(input):
    data = parseInput(input)
    end = (len(data[0]) - 1, len(data) - 1)
    result = solve(data, (0, 0), end, solveNode2)
    return result

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
4322674655533"""), 94)
        
    def test_part2_2(self):
        self.assertEqual(parse2("""111111111111
999999999991
999999999991
999999999991
999999999991"""), 71)

unittest.main(exit=False)

with open('input17.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

