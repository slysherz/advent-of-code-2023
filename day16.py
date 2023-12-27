import unittest

UP = '^'
DOWN = '∨'
LEFT = '<'
RIGHT = '>'

DIRECTION = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0)
}
SPLIT = {
    ('|', LEFT): [UP, DOWN],
    ('|', RIGHT): [UP, DOWN],
    ('-', UP): [LEFT, RIGHT],
    ('-', DOWN): [LEFT, RIGHT],
    ('/', RIGHT): [UP],
    ('/', LEFT): [DOWN],
    ('/', DOWN): [LEFT],
    ('/', UP): [RIGHT],
    ('\\', RIGHT): [DOWN],
    ('\\', LEFT): [UP],
    ('\\', DOWN): [RIGHT],
    ('\\', UP): [LEFT],
}

def validPosition(board, pos):
    x, y = pos
    return x >= 0 and x < len(board[0]) and y >= 0 and y < len(board)

def parseInput(input):
    return [line for line in input.splitlines()]

def solve(data, start):
    rays = [start]
    visited = {}
    visi_board = [[' ' for _ in line] for line in data]
    
    while len(rays):
        new_rays = []
        for pos, dir in rays:
            key = (pos, dir)
            if key in visited: continue
            visi_board[pos[1]][pos[0]] = '#'
            visited[key] = True

            x, y = pos
            c = data[y][x]
            if (c, dir) in SPLIT:
                next = SPLIT[(c, dir)]
            else:
                next = [dir]

            for c1 in next:
                dx, dy = DIRECTION[c1]
                npos = (x + dx, y + dy)
                if validPosition(data, npos):
                    new_rays.append((npos, c1))
        rays = new_rays

    visited_pos = {}
    for pos, dir in visited: visited_pos[pos] = True

    return len(visited_pos)

def parse1(input):
    data = parseInput(input)
    return solve(data, ((0, 0), RIGHT))

def parse2(input):
    data = parseInput(input)
    best = 0
    for x in range(0, len(data[0])):
        best = max(best, solve(data, ((x, 0), DOWN)))
        best = max(best, solve(data, ((x, len(data) - 1), UP)))
        
    for y in range(0, len(data)):
        best = max(best, solve(data, ((0, y), RIGHT)))
        best = max(best, solve(data, ((len(data[0]) - 1, y), LEFT)))
    return best

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1(""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""), 46)
        
    
    def test_part2(self):
        self.assertEqual(parse2(""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""), 51)

unittest.main(exit=False)

with open('input16.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

