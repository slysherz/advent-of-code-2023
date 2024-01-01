import unittest
import re

def parseInput(input):
    workflows = {}
    values = []
    for line in input.splitlines():
        m1 = re.match(r'\{((\w=\d+,?){4})\}', line)
        m2 = re.match(r'(\w+)\{(.+)\}', line)
        if m1 != None:
            entry = {}
            for var, val in re.findall(r'(\w)=(\d+)', m1[1]):
                entry[var] = int(val)
            values.append(entry)
        elif m2:
            rule_name = m2[1]
            rules = []
            for xp in m2[2].split(','):
                m3 = re.match(r'(\w+)([<>])(\d+):(\w+)', xp)
                if m3 != None:
                    rules.append((m3[1], m3[2], int(m3[3]), m3[4]))
                    pass
                else:
                    rules.append(xp)
            workflows[rule_name] = rules
    return (workflows, values)

def solveValue(workflows, value):
    wf = 'in'
    while True:
        for rule in workflows[wf]:
            if rule == 'A' or rule == 'R':
                return rule
            if isinstance(rule, str):
                wf = rule
                break

            var, op, val, res = rule
            if op == '<' and value[var] < val or op == '>' and value[var] > val:
                if res == 'A' or res == 'R':
                    return res
                wf = res
                break
        else:
            assert(False)
    
def parse1(input):
    data = parseInput(input)
    workflows, values = data

    result = 0
    for val in values:
        res = solveValue(workflows, val)
        if res == 'A':
            result += val['x'] + val['m'] + val['a'] + val['s']

    return result

def splitValueAt(value, var, val):
    new = value.copy()
    min, max = value[var]
    if min < val:
        value[var] = (min, val)
    else:
        value = None
    if val < max:
        new[var] = (val, max)
    else:
        new = None
    return (value, new)

def solveValue2(workflows, value, start = 'in'):
    if value == None or start == 'R': return 0
    if start == 'A':
        a, b, c, d = value.values()
        assert(a[1] > a[0] and b[1] > b[0] and c[1] > c[0] and d[1] > d[0])
        res = (a[1] - a[0]) * (b[1] - b[0]) * (c[1] - c[0]) * (d[1] - d[0])
        return res

    wf = start
    result = 0
    for rule in workflows[wf]:
        if isinstance(rule, str):
            result += solveValue2(workflows, value, rule)
            break

        var, op, val, res = rule
        if op == '<':
            new, value = splitValueAt(value, var, val)
            result += solveValue2(workflows, new, res)
        elif op == '>':
            value, new = splitValueAt(value, var, val + 1)
            result += solveValue2(workflows, new, res)
        else: assert(False)

    return result

def parse2(input):
    data = parseInput(input)
    workflows, values = data
    value = {
        'x': (1, 4001),
        'm': (1, 4001),
        'a': (1, 4001),
        's': (1, 4001)
    }

    return solveValue2(workflows, value)

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""), 19114)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}"""), 167409079868000)

unittest.main(exit=False)

with open('input19.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

