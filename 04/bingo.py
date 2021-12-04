import re

def won(board, nums):
    size = len(board)
    for i in range(size):
        if all(board[i][j] in nums for j in range(size)):
            return True
        if all(board[j][i] in nums for j in range(size)):
            return True
    return False

def unmarked(board, nums):
    return sum([n for line in board for n in line if n not in nums])

class Bingo:
    def __init__(self, file):
        f = open('04/'+file).readlines()

        self.nums = list(map(int, f[0].split(',')))
        self.boards = []

        i = 2
        board = []

        while i < len(f):

            if len(f[i]) > 2:
                line = list(map(int,re.findall(r'(\d+)', f[i])))
                board.append(line)
            else:
                self.boards.append(board)
                board = []

            i += 1
            
        if len(board) > 0:
            self.boards.append(board)

    def score(self):
        round = 1

        while True:
            for b in self.boards:
                if won(b, self.nums[:round]):
                    return unmarked(b, self.nums[:round]) * self.nums[round-1]
            round += 1

    def last(self):
        round = 1
        boards = self.boards

        while True:
            newBoards = []
            for b in boards:
                if won(b, self.nums[:round]):
                    if len(boards) == 1:
                        return unmarked(b, self.nums[:round]) * self.nums[round-1]
                else:
                    newBoards.append(b)
            boards = newBoards
            round += 1

b = Bingo('test.txt')
assert b.score() == 4512
assert b.last() == 1924

b = Bingo('input.txt')
print(b.score())
print(b.last())