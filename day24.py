import unittest

def parseInput(input):
    result = []
    for line in input.splitlines():
        pos, vel = line.split('@')
        result.append((
            tuple(int(s) for s in pos.split(', ')),
            tuple(int(s) for s in vel.split(', '))
        ))
    return result

def vecToFunc(h):
    pos, vel = h
    x, y, _ = pos
    vx, vy, _ = vel

    if vx == 0 and vy > 0:
        return float('inf')
    if vx == 0:
        return float('-inf')
    m = vy / vx
    t = -x / vx
    b = y + vy * t

    return (m, b)


# x0 + v0 * t = x1 + v1 * t <=>
# (v0 - v1) * t = x1 - x0 <=>
# t = (x1 - x0) / (v0 - v1)
def intersect(h0, h1):
    m0, b0 = vecToFunc(h0)
    m1, b1 = vecToFunc(h1)

    if m0 == m1:
        return None

    x = (b1 - b0) / (m0 - m1)

    if (x - h0[0][0]) / h0[1][0] < 0: return None
    if (x - h1[0][0]) / h1[1][0] < 0: return None

    return x

def parse1(input, start, end):
    data = parseInput(input)
    result = 0
    for i, h0 in enumerate(data):
        for h1 in data[i + 1:]:
            inter = intersect(h0, h1)
            if inter != None:
                # print(inter)
                if inter >= start and inter <= end:
                    result += 1
    return result

def parse2(input):
    data = parseInput(input)
    return 0

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""", 7, 27), 2)
    
    # def test_part2(self):
    #     self.assertEqual(parse2(""" """), 0)

unittest.main(exit=False)

with open('input24.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data, 200000000000000, 400000000000000))
    print("Part 2:", parse2(data))

