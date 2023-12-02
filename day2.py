import re
import unittest

def parseInput(input):
    games = []
    for line in input.splitlines():
        m = re.match(r'Game (\d+): (.+)', line)
        id = m.group(1)
        rest = m.group(2)
        rounds = []
        for round_str in rest.split('; '):
            round = []
            for picked_str in round_str.split(', '):
                pm = re.match(r'(\d+) (\w+)', picked_str)
                round.append((
                    int(pm.group(1)),
                    pm.group(2),
                ))
            rounds.append(round)
        games.append((
            int(id),
            rounds
        ))

    return games

MAX_PICKED = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def countCubes(round):
    result = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for n, color in round:
        result[color] += n

    return result

def isPossibleGame(rounds):
    for round in rounds:
        res = countCubes(round)
        if res['red'] > MAX_PICKED['red'] or res['green'] > MAX_PICKED['green'] or res['blue'] > MAX_PICKED['blue']:
            return False
        
    return True

def parse1(input):
    result = 0
    for id, rounds in parseInput(input):
        if isPossibleGame(rounds):
            result += id
        
    return result

def parse2(input):
    result = 0
    for id, rounds in parseInput(input):
        cubes = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for round in rounds:
            for n, color in round:
                cubes[color] = max(cubes[color], n)
        power = cubes['red'] * cubes['green'] * cubes['blue']
        result += power
            
    return result

class Test(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(parse1("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""), 8)
        
    
    def test_part2(self):
        self.assertEqual(parse2("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""), 2286)

unittest.main(exit=False)

with open('input2.txt') as file:
    data = file.read()
    print(parse1(data))
    print(parse2(data))

