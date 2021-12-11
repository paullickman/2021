import collections
from enum import Enum

score = {')': 3, ']': 57, '}': 1197, '>': 25137}

pair = {')': '(', ']': '[', '}': '{', '>': '<'}
close = {}
for p in pair.keys():
    close[pair[p]] = p

points = {')': 1, ']': 2, '}': 3, '>': 4}

class Result(Enum):
    OK = 1
    INCOMPLETE = 2
    CORRUPT = 3

def analyse(line):
    d = collections.deque()
    for c in line:
        if c in '([{<':
            d.append(c)
        else:
            if not d:
                return (Result.CORRUPT,c)
            else:
                p = d.pop()
                if pair[c] != p:
                    return (Result.CORRUPT,c)
    if not d:
        return (Result.OK,)
    else:
        return (Result.INCOMPLETE,d)

class Syntax():
    def __init__(self,file):
        self.lines = [l.strip() for l in open('10/'+file).readlines()]

    def corrupt(self):
        total = 0
        for line in self.lines:
            a = analyse(line)
            if a[0] == Result.CORRUPT:
                total += score[a[1]]
        return total

    def incomplete(self):
        scores = []
        for line in self.lines:
            a = analyse(line)
            if a[0] == Result.INCOMPLETE:
                s = 0
                while a[1]:
                    s = s*5 + points[close[a[1].pop()]]
                scores.append(s)
        scores.sort()
        return scores[len(scores)//2]



s = Syntax('test.txt')
assert s.corrupt() == 26397
assert s.incomplete() == 288957

s = Syntax('input.txt')
print(s.corrupt())
print(s.incomplete())
