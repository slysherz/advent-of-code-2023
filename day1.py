import re
import unittest

def parse1(input):
    result = 0
    for line in input.splitlines():
        for c in line:
            if c.isdigit():
                result += 10 * int(c)
                break
        for c in reversed(line):
            if c.isdigit():
                result += int(c)
                break
    return result

digits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def parseDigit(digit_str):
    if digit_str.isdigit():
        return int(digit_str)
    else:
        return digits[digit_str]

def parse2(input):
    result = 0
    for line in input.splitlines():
        assert(len(line.strip()) > 0)
        digit_one = re.search(r'(\d|one|two|three|four|five|six|seven|eight|nine)', line).group()
        digit_two = re.search(r'.*(\d|one|two|three|four|five|six|seven|eight|nine).*$', line).group(1)
        result += 10 * parseDigit(digit_one) + parseDigit(digit_two)
    return result


class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""), 142)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""), 281)

unittest.main(exit=False)

with open('input1.txt') as file:
    data = file.read()
    print(parse1(data))
    print(parse2(data))

