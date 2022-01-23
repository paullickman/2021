import copy

class Map():
    def __init__(self, file):
        lines = open('25/' + file).readlines()
        self.map = [list(line.strip()) for line in lines]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def print(self):
        for line in self.map:
            print(''.join(line))
        print

    def move(self, cucumber, xDiff, yDiff):
        newMap = copy.deepcopy(self.map)
        moved = False
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == cucumber:
                    xNew = (x + xDiff) % self.width
                    yNew = (y + yDiff) % self.height
                    if self.map[yNew][xNew] == '.':
                        newMap[yNew][xNew] = cucumber
                        newMap[y][x] = '.'
                        moved = True
        self.map = newMap
        return moved

    def step(self):
        moved = self.move('>',1,0)
        moved = self.move('v',0,1) or moved
        return moved

    def iterate(self):
        steps = 1
        while self.step():
            steps += 1
        return steps

m = Map('test.txt')
assert m.iterate() == 58

m = Map('input.txt')
print(m.iterate())