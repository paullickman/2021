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

    def quantum(self):
        maxScore = 30
        cache = [[[[[[0 for _ in range(3)] for _ in range(maxScore+1)] for _ in range(maxScore+1)] for _ in range(11)] for _ in range(11)] for _ in range(3)]

        # cache [p][p1][p2][s1][s2][n] is the number of winning ways for player n, given:
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
                                    cache[1][p1][p2][s1][s2][1] += 1
                                    cache[2][p1][p2][s1][s2][1] += 1
                            else:
                                if s2 < 21:
                                    for roll1 in range(1,4):
                                        for roll2 in range(1,4):
                                            for roll3 in range(1,4):
                                                # Player 1 move
                                                pos = (p1 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                                for n in [1,2]:
                                                    cache[1][p1][p2][s1][s2][n] += cache[2][pos][p2][s1+pos][s2][n]
                                                # Player 2 move
                                                pos = (p2 + roll1 + roll2 + roll3 - 1) % 10 + 1
                                                for n in [1,2]:
                                                    cache[2][p1][p2][s1][s2][n] += cache[1][p1][pos][s1][s2+pos][n]
                                else:
                                    cache[1][p1][p2][s1][s2][2] += 1
                                    cache[2][p1][p2][s1][s2][2] += 1

        return [cache[1][self.initPositions[0]][self.initPositions[1]][0][0][1], cache[1][self.initPositions[0]][self.initPositions[1]][0][0][2]]

g1 = Game('test.txt')
assert g1.play() == 739785

g2 = Game('input.txt')
print(g2.play())

assert g1.quantum() == [444356092776315, 341960390180808]

print(max(g2.quantum()))