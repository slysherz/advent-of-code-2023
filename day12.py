import unittest
from functools import cache

def parseInput(input, repeats):
    result = []

    for line in input.splitlines():
        springs, ns = line.split(' ')
        result.append((((springs + '?') * repeats)[:-1], [int(n) for n in ns.split(',')] * repeats))

    return result

def solveLine(string, count):
    spring = ['?', '#']
    empty = ['?', '.']

    @cache
    def solve(i, j):
        if j == len(count):
            if any(c == '#' for c in string[i:]):
                return 0
            return 1
        if i == len(string):
            return 0
        min_size = sum(n + 1 for n in count[j:]) - 1
        if min_size > len(string) - i:
            return 0

        result = 0
        block = count[j]
        if all(string[k] in spring for k in range(i, i + block)) and (
            i + block == len(string) or string[i + block] in empty
        ):
            result += solve(i + block + 1, j + 1)
        if string[i] in empty:
            result += solve(i + 1, j)

        return result
    return solve(0, 0)

def parse(input, repeats):
    data = parseInput(input, repeats)
    result = 0
    for i, e in enumerate(data):
        line, ns = e
        result += solveLine(line, ns)
    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 1), 21)
        
    def test_part2(self):
        self.assertEqual(parse("""???.### 1,1,3""", 5), 1)
        self.assertEqual(parse(""".??..??...?##. 1,1,3""", 5), 16384)
        self.assertEqual(parse("""?#?#?#?#?#?#?#? 1,3,1,6""", 5), 1)
        self.assertEqual(parse("""????.#...#... 4,1,1""", 5), 16)
        self.assertEqual(parse("""????.######..#####. 1,6,5""", 5), 2500)
        self.assertEqual(parse("""?###???????? 3,2,1""", 5), 506250)
        self.assertEqual(parse("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 5), 525152)

unittest.main(exit=False)

with open('input12.txt') as file:
    data = file.read()
    print("Part 1:", parse(data, 1))
    print("Part 2:", parse(data, 5))

