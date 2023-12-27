import unittest
import re

def parseInput(input):
    result = []
    expr: str
    for expr in input.strip().split(','):
        result.append(expr)
    return result

def hash(string):
    value = 0
    for c in string:
        n = ord(c)
        value = (value + n) * 17 % 256
    return value

def parse1(input):
    data = parseInput(input)
    return sum(hash(s) for s in data)

def parse2(input):
    data = parseInput(input)
    boxes = {}
    for expr in data:
        if expr.endswith('-'):
            name = expr[:-1]
            box = hash(name)
            if not box in boxes: boxes[box] = []
            boxes[box] = [(n, v) for n, v in boxes[box] if n != name]
        else:
            name, vstr = expr.split('=')
            value = int(vstr)
            box = hash(name)
            if not box in boxes: boxes[box] = []
            if any(name == n for n, v in boxes[box]):
                boxes[box] = [(n, v) if n != name else (name, value) for n, v in boxes[box]]
            else:
                boxes[box].append((name, value))

    result = 0
    for box in boxes:
        for i, val in enumerate(boxes[box]):
            _, value = val
            result += (box + 1) * (i + 1) * value

    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""), 1320)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""), 145)

unittest.main(exit=False)

with open('input15.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

