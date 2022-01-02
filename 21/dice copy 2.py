from functools import lru_cache
import re

class Game():
    def __init__(self, file):
        lines = [re.findall(r'(\d+)', line.strip()) for line in open('21/' + file).readlines()]

        self.initPositions = [int(lines[0][1]), int(lines[1][1])]
        self.scores = [0,0]

        self.dice = 1

    def roll(self):
        while True:
            yield self.dice

            self.dice = self.dice % 100 + 1

    def play(self):
        dice = self.roll()
        turn = 0
        numRolls = 0
        positions = self.initPositions[:]
        while self.scores[1-turn] < 1000:
            roll = next(dice) + next(dice) + next(dice)
            numRolls += 1
            positions[turn] = (positions[turn] + roll - 1) % 10 + 1
            self.scores[turn] += positions[turn]
            turn = 1-turn
        return self.scores[turn] * (numRolls * 3)

    def quantum(self, player):
        maxScore = 30
        cache = [[[[[0 for _ in range(maxScore+1)] for _ in range(maxScore+1)] for _ in range(11)] for _ in range(11)] for _ in range(3)]

        # cache [p][p1][p2][s1][s2] is the number of winning ways for player 1, given:
            # player p to play next
            # player 1 at position p1
            # player 2 at position p2
            # player 1 has score s1
            # player 2 has score s2

        # Pre-cache
        # Iterate over all scoring pairs largest first i.e. diagonal pattern

        for scoreSum in range(maxScore*2, -1, -1):
            for s1 in range(maxScore, -1, -1):
                s2 = scoreSum - s1
                if s2 >= 0 and s2 <= maxScore:
                    for p1 in range(1,11):
                        for p2 in range(1,11):
                            if s1 >= 21:
                                if s2 < 21:
                                    cache[1][p1][p2][s1][s2] = 1
                                    cache[2][p1][p2][s1][s2] = 1
                            else:
                                if s2 < 21:
                                    for roll1 in range(1,4):
                                        for roll2 in range(1,4):
                                            for roll3 in range(1,4):
                                                # Player 1 move
                                                pos = (p1 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                                cache[1][p1][p2][s1][s2] += cache[2][pos][p2][s1+pos][s2]
                                                # Player 2 move
                                                pos = (p2 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                                cache[2][p1][p2][s1][s2] += cache[1][p1][pos][s1][s2+pos]
                                else:
                                    cache[1][p1][p2][s1][s2] = 0 # Change these to 1 for all games and 0 for just player 1
                                    cache[2][p1][p2][s1][s2] = 0



g = Game('test.txt')
assert g.play() == 739785

g = Game('input.txt')
print(g.play())

maxScore = 30
cache = [[[[[0 for _ in range(maxScore+1)] for _ in range(maxScore+1)] for _ in range(11)] for _ in range(11)] for _ in range(3)]

# cache [p][p1][p2][s1][s2] is the number of winning ways for player 1, given:
    # player p to play next
    # player 1 at position p1
    # player 2 at position p2
    # player 1 has score s1
    # player 2 has score s2

# Pre-cache
# Iterate over all scoring pairs largest first i.e. diagonal pattern

for scoreSum in range(maxScore*2, -1, -1):
    for s1 in range(maxScore, -1, -1):
        s2 = scoreSum - s1
        if s2 >= 0 and s2 <= maxScore:
            for p1 in range(1,11):
                for p2 in range(1,11):
                    if s1 >= 21:
                        if s2 < 21:
                            cache[1][p1][p2][s1][s2] = 1
                            cache[2][p1][p2][s1][s2] = 1
                    else:
                        if s2 < 21:
                            for roll1 in range(1,4):
                                for roll2 in range(1,4):
                                    for roll3 in range(1,4):
                                        # Player 1 move
                                        pos = (p1 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                        cache[1][p1][p2][s1][s2] += cache[2][pos][p2][s1+pos][s2]
                                        # Player 2 move
                                        pos = (p2 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                        cache[2][p1][p2][s1][s2] += cache[1][p1][pos][s1][s2+pos]
                        else:
                            cache[1][p1][p2][s1][s2] = 0 # Change these to 1 for all games and 0 for just player 1
                            cache[2][p1][p2][s1][s2] = 0

print(cache[1][4][8][0][0])
# player 1 444356092776315
# player 2 341960390180808

print(cache[1][5][8][0][0])

# 630947104784464
