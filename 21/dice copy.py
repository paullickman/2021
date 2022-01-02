from functools import lru_cache
import re

class Game():
    def __init__(self, file):
        lines = [re.findall(r'(\d+)', line.strip()) for line in open('21/' + file).readlines()]

        self.positions = [int(lines[0][1]), int(lines[1][1])]
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
        while self.scores[1-turn] < 1000:
            roll = next(dice) + next(dice) + next(dice)
            numRolls += 1
            self.positions[turn] = (self.positions[turn] + roll - 1) % 10 + 1
            self.scores[turn] += self.positions[turn]
            turn = 1-turn
        return self.scores[turn] * (numRolls * 3)

# g = Game('test.txt')
# assert g.play() == 739785

# g = Game('input.txt')
# print(g.play())

@lru_cache
def wins(turn, pos1, pos2, score1, score2):
    if turn == 1: # Player 1
        if score2 >= 21:
            return 1
        if score1 >= 21:
            return 0
        p1 = pos1 % 10 + 1
        p2 = p1 % 10 + 1
        p3 = p2 % 10 + 1
        return wins(3-turn, p1, pos2, score1+1, score2) + wins(3-turn, p2, pos2, score1+2, score2) + wins(3-turn, p3, pos2, score1+3, score2)
    else: # Player 2
        if score1 >= 21:
            return 1
        if score2 >= 21:
            return 0
        p1 = pos1 % 10 + 1
        p2 = p1 % 10 + 1
        p3 = p2 % 10 + 1
        return wins(3-turn, pos1, p1, score1, score2+1) + wins(3-turn, pos1, p2, score1, score2+2) + wins(3-turn, pos1, p3, score1, score2+3)

print('start')

# Pre-cache
for score in range(20, 0, -1):
    print(score)
    for p1 in range(1,11):
        for p2 in range(1,11):
            for s in range(score+1, 21):
                for player in [1,2]:
                    wins(player,p1,p2, score, s)
                    wins(player,p1,p2, s, score)
                    wins(player,p1,p2, score, score)

# for score in range(20, 0, -1):
#     print(score, wins(1,4,8,score,score))

print(wins(1,4,8,0,0))

print('end')