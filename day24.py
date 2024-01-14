import unittest
from collections import Counter

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

    assert vx != 0 or vy != 0
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
    y0 = m0 * x + b0
    y1 = m1 * x + b1

    if (x - h0[0][0]) / h0[1][0] < 0: return None
    if (x - h1[0][0]) / h1[1][0] < 0: return None

    return (x, y0, y1)

def parse1(input, start, end):
    data = parseInput(input)
    result = 0
    for i, h0 in enumerate(data[:-1]):
        for j, h1 in enumerate(data[i + 1:]):
            inter = intersect(h0, h1)
            if inter != None:
                x, y0, y1 = inter
                if x >= start and x <= end and y0 >= start and y0 <= end and y1 >= start and y1 <= end:
                    result += 1
    return result

def sub(h0, h1):
    return (h0[0] - h1[0], h0[1] - h1[1], h0[2] - h1[2])

def findVelocity(data, axis):
    vxs = dict(Counter(h[1][axis] for h in data))
    vxs = { k: vxs[k] for k in sorted(vxs, key= lambda k: vxs[k], reverse=True) if vxs[k] > 1 }
    vxs = { vx: [h[0][axis] for h in data if h[1][axis] == vx] for vx in vxs }

    for rvx in range(1000000):
        failed = False

        for vx, hs in vxs.items():
            if not all(rvx == vx or x % (rvx - vx) == hs[0] % (rvx - vx) for x in hs[1:]):
                failed = True
                break
            if vx == rvx and any(hs[0] != x for x in hs):
                failed = True
                break

        if not failed:
            return rvx
    assert False, 'Cannot get here'

def parse2(input):
    data = sorted(parseInput(input))
    min_x = min(h[0][0] for h in data)
    min_y = min(h[0][1] for h in data)
    min_z = min(h[0][2] for h in data)
    min_p = (min_x, min_y, min_z)

    min_vx = min(h[1][0] for h in data)
    min_vy = min(h[1][1] for h in data)
    min_vz = min(h[1][2] for h in data)
    min_v = (min_vx, min_vy, min_vz)

    # Change referential to make things simpler
    data = [(sub(h[0], min_p), sub(h[1], min_v)) for h in data]

    vel = tuple([findVelocity(data, axis) for axis in range(3)])
    rz = [
        h[0][2]
        for h in data
        if h[1][2] == vel[2]
    ][0]

    # Pick a rock
    h0 = data[0]
    assert h0[1][2] != vel[2], 'Must have different velocity'

    t = (rz - h0[0][2]) // (h0[1][2] - vel[2])
    rx = h0[0][0] + h0[1][0] * t - vel[0] * t
    ry = h0[0][1] + h0[1][1] * t - vel[1] * t

    return rx + ry + rz + min_x + min_y + min_z

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""", 7, 27), 2)

unittest.main(exit=False)

with open('input24.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data, 200000000000000, 400000000000000))
    print("Part 2:", parse2(data))

