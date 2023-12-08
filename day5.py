import unittest
import re

def parseNumbers(string):
    return list(map(int, string.split(' ')))

def parseBlock(string):
    lines = string.splitlines()

    m = re.match(r'(\w+)-to-(\w+) map:', lines[0])
    return sorted([parseNumbers(s) for s in lines[1:]])

def resolveBlock(block, input):
    for e, s, l in block:
        if input >= s and input < s + l:
            return input - s + e
    return input

def parseInput(input):
    blocks_str = re.split(r'[\r\n]{2}', input)
    seeds = parseNumbers(blocks_str[0][7:])

    blocks = [parseBlock(b) for b in blocks_str[1:]]

    return (seeds, blocks)

def parse1(input):
    seeds, blocks = parseInput(input)
    result = float('inf')
    for current in seeds:
        for block in blocks:
            current = resolveBlock(block, current)
            
        result = min(result, current)

    return result

def intersect(s1, l1, s2, l2):
    e1 = s1 + l1
    e2 = s2 + l2
    start = max(s1, s2)
    end = min(e1, e2)
    count = end - start
    if count <= 0:
        return None
    return (start, count)

def findMin(ctx, start, count, i):
    # print('{}[{}, {}]'.format(' ' * (4 * (6-i)), start, start + count))
    if count <= 0:
        return None

    seeds, blocks = ctx
    if i == -1:
        for j in range(0, len(seeds), 2):
            e = seeds[j]
            l = seeds[j + 1]
            shared = intersect(start, count, e, l)
            if shared != None:
                return shared[0]

        return None

    index = 0
    block = blocks[i]
    for e, s, l in block:
        if e > index:
            # Search before the current block
            ce = index
            cl = e - index
            shared = intersect(start, count, ce, cl)
            if shared != None:
                temp = findMin(ctx, shared[0], shared[1], i - 1)
                if temp != None:
                    return temp

        # Search current block
        shared = intersect(start, count, e, l)
        ofset = s - e
        if shared != None:
            temp = findMin(ctx, shared[0] + ofset, shared[1], i - 1)
            if temp != None: return temp - ofset

        index = e + l + 1

    shared = intersect(start, count, index, float('inf'))
    if shared:
        return findMin(ctx, shared[0], shared[1], i - 1)
    
    return None

def parse2(input):
    ctx = parseInput(input)
    return findMin(ctx, 0, float('inf'), len(ctx[1]) - 1)

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""), 35)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""), 46)

unittest.main(exit=False)

with open('input5.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

