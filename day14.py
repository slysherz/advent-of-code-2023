import unittest

O = 'O'

def parseInput(input):
    result = []
    for line in input.splitlines():
        result.append(list(line))
    return result

def tilt(data):
    width = len(data[0])
    height = len(data)

    for x in range(0, width):
        for y in range(0, height):
            c = data[y][x]
            if c == O or c == '#': continue
            for y1 in range(y + 1, height):
                c1 = data[y1][x]
                if c1 == '#': break
                if c1 == O:
                    data[y][x] = O
                    data[y1][x] = '.'
                    break

def rotate(data):
    return list(list(a) for a in zip(*data[::-1]))

def score(data):
    width = len(data[0])
    height = len(data)
    result = 0
    for x in range(0, width):
        for y in range(0, height):
            c = data[y][x]
            if c == O:
                result += height - y
    return result

def printBoard(data):
    for row in data: print(''.join(row))
    print()

def parse1(input):
    data = parseInput(input)
    tilt(data)
    return score(data)

def runFor(data, rounds):
    scores = {}
    for i in range(0, rounds):
        key = tuple(tuple(row) for row in data)
        if key in scores:
            k = scores[key]
            steps_left = rounds - k
            cycle_size = i - k
            steps_after = steps_left % cycle_size
            return runFor(data, steps_after)
        scores[key] = i
        for j in range(0, 4):
            tilt(data)
            data = rotate(data)

    return score(data)

def parse2(input):
    data = parseInput(input)
    rounds = 1000000000
    return runFor(data, rounds)


class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""), 136)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""), 64)

unittest.main(exit=False)

with open('input14.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

