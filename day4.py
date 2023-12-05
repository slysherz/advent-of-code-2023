import unittest
import re

def listMap(fn, it):
    return list(map(fn, it))

def parseInput(input):
    cards = []
    for line in input.splitlines():
        m = re.match(r'Card\s+\d+:\s+(.+) \|\s+(.+)', line)
        nyh = listMap(int, re.split(r'\s+', m.group(1)))
        wn = listMap(int, re.split(r'\s+', m.group(2)))
        cards.append((nyh, wn))

    return cards

def countWinningNumbers(card):
    nyh, wn = card
    return sum(1 for i in wn if i in nyh)

def parse1(input):
    cards = parseInput(input)
    wins = map(countWinningNumbers, cards)
    return sum(pow(2, w - 1) if w > 0 else 0 for w in wins)

def parse2(input):
    cards = parseInput(input)
    counts = [1 for c in cards]

    result = 0
    for i in range(0, len(counts)):
        result += counts[i]
        w = countWinningNumbers(cards[i])
        for j in range(i + 1, i + w + 1):
            counts[j] += counts[i]

    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""), 13)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""), 30)

unittest.main(exit=False)

with open('input4.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

