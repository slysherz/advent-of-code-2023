import unittest
import bisect 
import random

def parseInput(input):
    result = []
    for line in input.splitlines():
        start, end = line.split('~')
        result.append((
            tuple(map(int, start.split(','))),
            tuple(map(int, end.split(',')))
        ))

    result.sort(key= lambda brick: min(brick[0][2], brick[1][2]))
    return result

def colisionPattern(block):
    result = 0
    start, end = block
    for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
        for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
            result ^= 1 << 10 * y + x
    return result

def intersect(a, b):
    return a & b != 0

def stackBricks(input):
    data = parseInput(input)

    ground = []
    supported = []
    for i, block in enumerate(data):
        cp = colisionPattern(block)
        end_pos = 0
        for top_h, j, ocp in reversed(ground):
            if top_h < end_pos: break
            if intersect(cp, ocp):
                end_pos = top_h
                supported.append((j, i))

        height = block[1][2] - block[0][2]
        bisect.insort(ground, (end_pos + height + 1, i, cp))

    supported.sort()
    supporting = {
        d1: [u2 for d2, u2 in supported if d1 == d2]
        for d1, u1 in supported
    }
    need_support = {
        u1: [d2 for d2, u2 in supported if u1 == u2]
        for _, u1 in supported
    }
    
    return data, supporting, need_support

def parse1(input):
    data, supporting, need_support = stackBricks(input)
    
    removeable = [
        k
        for k, v in supporting.items()
        if any(len(need_support[i]) == 1 for i in v)
    ]

    return len(data) - len(removeable)

def crumble(supporting, need_support, i, cache = {}):
    result = set()
    if not i in supporting: return result
    if i in cache: return cache[i]

    for j in supporting[i]:
        if len(need_support[j]) == 1:
            result.add(j)
            result.update(crumble(supporting, need_support, j))

    while True:
        new_entries = set()
        for k in result:
            if not k in supporting: continue
            for l in supporting[k]:
                if l in result: continue
                if all(m in result for m in need_support[l]):
                    new_entries.add(l)
                    new_entries.update(crumble(supporting, need_support, l))
        if len(new_entries):
            result.update(new_entries)
        else:
            break
    cache[i] = result
    return result

def parse2(input):
    data, supporting, need_support = stackBricks(input)
    return sum(len(crumble(supporting, need_support, i)) for i, _ in enumerate(data))

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""), 5)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""), 7)

unittest.main(exit=False)

with open('input22.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

