import unittest

NB_CARDS = 13
CARD_TO_KEY = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 9,
    'T': 8,
}

def cardToKey(card):
    if card in CARD_TO_KEY:
        return CARD_TO_KEY[card]
    return int(card) - 2

def parseInput(input):
    result = []
    for line in input.splitlines():
        sc, sb = line.split(' ')
        cards = list(sc)
        result.append((cards, int(sb)))

    return result

def countRepeats(cards):
    count = {}

    for c in cards:
        if not c in count: count[c] = 0
        count[c] += 1

    return list(sorted(count.values(), reverse=True))

def cardsScore(sc):
    c = countRepeats(sc)

    # Five of a kind
    if c[0] == 5: return 6

    # Four of a kind
    if c[0] == 4: return 5

    # Full house
    if c[0] == 3 and c[1] == 2: return 4

    # Three of a kind
    if c[0] == 3: return 3

    # Two pair
    if c[0] == 2 and c[1] == 2:
        return 2
    
    # One pair
    if c[0] == 2:
        return 1
    
    # Highest card
    return 0

def handToKey(hand):
    cards, _ = hand
    sc = sorted(cards, key=cardToKey, reverse=True)

    result = cardsScore(sc)
    for i in range(0, len(cards)):
        result = result * NB_CARDS + cardToKey(cards[i])
    
    return result

def parse1(input):
    data = parseInput(input)
    data.sort(key=handToKey)

    result = 0
    for i in range(0, len(data)):
        result += (i + 1) * data[i][1]

    return result

CARD_TO_KEY_J = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 0,
    'T': 9,
}

def countRepeatsJ(cards):
    count = {}

    for c in cards:
        if not c in count: count[c] = 0
        count[c] += 1

    js = count['J'] if 'J' in count else 0
    if 'J' in count: del count['J']    

    return (list(sorted(count.values(), reverse=True)), js)

def cardToKeyJ(card):
    if card in CARD_TO_KEY_J:
        return CARD_TO_KEY_J[card]
    return int(card) - 1

def cardsScoreJ(sc):
    c, js = countRepeatsJ(sc)

    # Five of a kind
    if js == 5 or c[0] + js == 5: return 6

    # Four of a kind
    if c[0] + js == 4: return 5

    # Full house
    if c[0] + js == 3 and c[1] == 2: return 4

    # Three of a kind
    if c[0] + js == 3: return 3

    # Two pair
    if c[0] == 2 and c[1] == 2:
        return 2
    
    # One pair
    if c[0] + js == 2:
        return 1
    
    # Highest card
    return 0

def handToKeyJ(hand):
    cards, _ = hand
    sc = sorted(cards, key=cardToKeyJ, reverse=True)

    result = cardsScoreJ(sc)
    for i in range(0, len(cards)):
        result = result * NB_CARDS + cardToKeyJ(cards[i])
    
    return result

def parse2(input):
    data = parseInput(input)
    data.sort(key=handToKeyJ)

    result = 0
    for i in range(0, len(data)):
        result += (i + 1) * data[i][1]

    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""), 6440)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""), 5905)

unittest.main(exit=False)

with open('input7.txt') as file:
    data = file.read()
    print("Part 1:", parse1(data))
    print("Part 2:", parse2(data))

