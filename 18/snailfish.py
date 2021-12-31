import re

def mag(s):
    c = next(s)
    if c.isnumeric():
        return int(c)
    else:
        leftNum = mag(s)
        next(s) # ,
        rightNum = mag(s)
        next(s) # ]
        return 3*leftNum + 2*rightNum

class SnailFish:
    def __init__(self, s):
        self.tokens = re.findall(r'\[|\]|\d+|\,', s)

    def __repr__(self):
        return ''.join(self.tokens)

    def __add__(self, s):
        addTokens = ['['] + self.tokens + [','] + s.tokens + [']']
        return SnailFish(''.join(addTokens))

    def searchLevel4(self):
        i = 0
        level = 0
        while i < len(self.tokens):
            if self.tokens[i] == '[':
                level += 1
            elif self.tokens[i] == ']':
                level -= 1
            if level > 4:
                return i
            i += 1
        return None

    def explode(self, i):
        # Look left
        leftNum = int(self.tokens[i+1])
        found = False
        j = i-1
        while not(found) and j>0:
            if self.tokens[j].isnumeric():
                self.tokens[j] = str(int(self.tokens[j]) + leftNum)
                found = True
            j -= 1

        # Look right
        rightNum = int(self.tokens[i+3])
        found = False
        j = i+4
        while not(found) and j<len(self.tokens):
            if self.tokens[j].isnumeric():
                self.tokens[j] = str(int(self.tokens[j]) + rightNum)
                found = True
            j += 1

        # Replace with 0
        self.tokens = self.tokens[:i] + ['0'] + self.tokens[i+5:]

    def searchTen(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].isnumeric() and int(self.tokens[i]) >= 10:
                return i
            i += 1
        return None

    def split(self, i):
        splitLeft = int(self.tokens[i]) // 2
        splitRight = (int(self.tokens[i]) + 1) // 2
        self.tokens = self.tokens[:i] + ['['] + [str(splitLeft)] + [','] + [str(splitRight)] + [']'] + self.tokens[i+1:]

    def reduce(self):
        repeat = True
        while repeat:
            repeat = False
            
            if (i := self.searchLevel4()) is not None:
                self.explode(i)
                repeat = True

            if not (repeat):
                if (i := self.searchTen()) is not None:
                    self.split(i)
                    repeat = True

    def magnitude(self):
        return mag(iter(self.tokens))

# Addition test case
s1 = SnailFish('[1,2]')
s2 = SnailFish('[[3,4],5]')
assert str(s1 + s2) == '[[1,2],[[3,4],5]]'

# Reduce test case

s1 = SnailFish('[[[[4,3],4],4],[7,[[8,4],9]]]')
s2 = SnailFish('[1,1]')
s3 = s1 + s2
s3.reduce()
assert str(s3) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

# Magnitude test cases

cases = \
[
('[9,1]', 29),
('[1,9]', 21),
('[[9,1],[1,9]]', 129),
('[[1,2],[[3,4],5]]', 143),
('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488)
]

for s, m in cases:
    s = SnailFish(s)
    assert s.magnitude() == m

def sumAll(file):
    lines = [SnailFish(line.strip()) for line in open('18/' + file).readlines()]
    s = lines[0]
    i = 1
    while i < len(lines):
        s += lines[i]
        s.reduce()
        i += 1
    return s.magnitude()

assert sumAll('test.txt') == 4140
print(sumAll('input.txt'))

def pair(file):
    lines = [SnailFish(line.strip()) for line in open('18/' + file).readlines()]
    maxPair = None
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i != j:
                s = lines[i] + lines[j]
                s.reduce()
                m = s.magnitude()
                if maxPair == None or m > maxPair:
                    maxPair = m
    return maxPair

assert pair('test.txt') == 3993
print(pair('input.txt'))