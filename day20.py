import unittest
import re

BC = 'B'
LOW = 0
HIGH = 1

def parseInput(input):
    result = {}
    for line in input.splitlines():
        m = re.match(r'(.+) -> (.+)', line)
        c = m[1][0]
        name = m[1][1:]
        if c == '%' or c == '&':
            module = c
        else:
            module = BC
            name = 'broadcaster'
        result[name] = (module, m[2].split(', '))
    return result

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sendPulse(data, memory, module, from_module, pulse):
    queue = [(from_module, pulse, module)]
    result = [0, 0]

    while len(queue):
        from_module, pulse, module = queue.pop(0)
        result[pulse] += 1
        # print('{} -{}-> {}'.format(from_module, ['low', 'high'][pulse], module), '\n')

        if not module in data: continue
        type, out = data[module]
        out_pulse = None
        if type == BC:
            out_pulse = LOW
        
        if type == '%':
            if pulse == LOW:
                memory[module] ^= 1
                out_pulse = memory[module]

        if type == '&':
            mem = memory[module]
            mem[from_module] = pulse
            out_pulse = LOW if all(mem[f] == HIGH for f in mem) else HIGH

        if out_pulse != None:
            for o in out:
                queue.append((module, out_pulse, o))

    return result

def parse1(input):
    data = parseInput(input)

    memory = {}
    for key in data:
        type, out = data[key]
        if type == '%': memory[key] = LOW
        if type == '&':
            mem = {}
            for key2 in data:
                for out in data[key2][1]:
                    if out == key:
                        mem[key2] = LOW
                        break
            memory[key] = mem
    
    result = (0, 0)
    for i in range(0, 1000):
        count = sendPulse(data, memory, 'broadcaster', 'button', LOW)
        result = add(result, count)

    return result[0] * result[1]

def parse2(input):
    return 0

class Test(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(parse1("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""), 32000000)

    def test_part1_2(self):
        self.assertEqual(parse1("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""), 11687500)

unittest.main(exit=False)

with open('input20.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

