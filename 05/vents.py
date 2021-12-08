import re

class Vents:
    def __init__(self, file):
        self.lines = list(map(lambda x: list(map(int, re.findall(r'(\d+)', x))), open('05/'+file).readlines()))

        self.maxX = max([line[i] for line in self.lines for i in [0,2]]) + 1
        self.maxY = max([line[i] for line in self.lines for i in [1,3]]) + 1

        self.overlaps = []
        for j in range(self.maxY):
            self.overlaps.append([0] * self.maxX)

        for line in self.lines:
            if line[0] == line[2]: # Vertical line
                if line[1] <= line[3]:
                    incr = 1
                else:
                    incr = -1
                for j in range(line[1], line[3]+incr, incr):
                    self.overlaps[j][line[0]] += 1
            elif line[1] == line[3]: # Horizontal line
                if line[0] <= line[2]:
                    incr = 1
                else:
                    incr = -1
                for i in range(line[0], line[2]+incr, incr):
                    self.overlaps[line[1]][i] += 1

    def addDiagonals(self):
        for line in self.lines:
            if (line[0] != line[2]) and (line[1] != line[3]): # Diagonal line
                if line[1] <= line[3]:
                    incrY = 1
                else:
                    incrY = -1
                    
                if line[0] <= line[2]:
                    incrX = 1
                else:
                    incrX = -1

                i = line[0]                    
                for j in range(line[1], line[3]+incrY, incrY):
                    self.overlaps[j][i] += 1
                    i += incrX

    def count(self):
        total = 0
        for i in range(self.maxY):
            for j in range(self.maxX):
                if self.overlaps[j][i] >= 2:
                    total += 1
        return total
        
v = Vents('test.txt')
assert v.count() == 5
v.addDiagonals()
assert v.count() == 12

v = Vents('input.txt')
print(v.count())
v.addDiagonals()
print(v.count())
