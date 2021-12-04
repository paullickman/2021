import re


class Submarine:
    def __init__(self, file):
        self.position = 0
        self.depth = 0

        course = [(i, int(n)) for i,n in re.findall(r'(\S+) (\d+)', open('02/'+file).read())]

        for i,n in course:
            match i:
                case 'forward':
                    self.position += n
                case 'down':
                    self.depth += n
                case 'up':
                    self.depth -= n

    def mult(self):
        return self.position * self.depth

# PRL Do inheritance

class Submarine2:
    def __init__(self, file):
        self.position = 0
        self.depth = 0
        self.aim = 0

        course = [(i, int(n)) for i,n in re.findall(r'(\S+) (\d+)', open('02/'+file).read())]

        for i,n in course:
            match i:
                case 'forward':
                    self.position += n
                    self.depth += self.aim * n
                case 'down':
                    self.aim += n
                case 'up':
                    self.aim -= n

    def mult(self):
        return self.position * self.depth

s = Submarine('test.txt')
assert s.mult() == 150

s = Submarine('input.txt')
print(s.mult())

s = Submarine2('test.txt')
assert s.mult() == 900

s = Submarine2('input.txt')
print(s.mult())

