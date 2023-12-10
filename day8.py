import unittest
import re
import itertools

def parseInput(input):
    dir = ""
    nodes = []

    for line in input.splitlines():
        m1 = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        m2 = re.match(r'[L|R]+', line)
        if m1 != None:
            nodes.append((m1.group(1), (m1.group(2), m1.group(3))))
        elif m2 != None:
            dir = m2.group(0)

    return (dir, nodes)

def nodeMap(nodes):
    node_map = {}
    for orig, dest in nodes:
        node_map[orig] = dest
    return node_map

def parse1(input):
    dir, nodes = parseInput(input)
    node_map = nodeMap(nodes)

    current = 'AAA'
    for i in itertools.count():
        if current == 'ZZZ': return i
        l, r = node_map[current]
        if dir[i % len(dir)] == 'L':
            current = l
        else:
            current = r

def minLoopReps(start, dir, node_map):
    trace = {}
    result = []
    
    current = start
    for i in itertools.count():
        j = i % len(dir)
        key = current, j
        if key in trace: return (i, trace[key], result)
        trace[key] = i

        if current[-1] == 'Z':
            result.append(i)

        l, r = node_map[current]
        if dir[j] == 'L':
            current = l
        else:
            current = r

# From stackoverflow
def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase

def arrow_alignment(red_len, green_len, advantage):
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period

def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

def parse2(input):
    dir, nodes = parseInput(input)
    node_map = nodeMap(nodes)

    current = [s for s in node_map.keys() if s[-1] == 'A']
    reps = [minLoopReps(c, dir, node_map) for c in current]

    temp = []
    for e, s, rep in reps:
        period = e - s
        temp.append((period, rep))

    res = (temp[0][0], temp[0][1][0])
    for period, rep in temp[1:]:
        for phase in rep:
            try:
                res = combine_phased_rotations(res[0], res[1], period, period - phase)
            except: pass

    return res[0]

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""), 6)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""), 6)

unittest.main(exit=False)

with open('input8.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

