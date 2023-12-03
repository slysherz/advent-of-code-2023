import unittest
import re

def parseInput(input):
    return list(input.splitlines())

def hasCloseSymbol(lines, li, l, r):
    line = lines[li]
    width = len(line)
    nb_lines = len(lines)
    for i in range(max(0, l - 1), min(width, r + 1)):
        for j in range(max(0, li - 1), min(nb_lines, li + 2)):
            if re.match(r'[^\d.]', lines[j][i]):
                return True

    return False

def parse1(input):
    lines = parseInput(input)
    result = 0

    for li in range(0, len(lines)):
        for m in re.finditer(r'(\d+)', lines[li]):
            n = int(m.group())
            if hasCloseSymbol(lines, li, m.start(), m.end()):
                result += n

    return result

def parseNumbers(line):
    numbers = []
    for m in re.finditer(r'(\d+)', line):
        numbers.append((
            int(m.group()),
            m.start(),
            m.end() - 1
        ))
    return numbers

def closeNumbers(numbers, x, y):
    result = []
    for i in range(max(0, y - 1), min(len(numbers), y + 2)):
        ns = numbers[i]
        for n, j, k in ns:
            if j - 1 <= x and x <= k + 1:
                result.append(n)

    return result

def parse2(input):
    lines = parseInput(input)
    numbers = list(map(parseNumbers, lines))
    result = 0

    for li in range(0, len(lines)):
        for m in re.finditer(r'\*', lines[li]):
            ns = closeNumbers(numbers, m.start(), li)

            if len(ns) == 2:
                result += ns[0] * ns[1]

    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""), 4361)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""), 467835)

unittest.main(exit=False)

with open('input3.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

