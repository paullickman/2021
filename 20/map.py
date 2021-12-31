from functools import lru_cache
import copy

@lru_cache
def binary(s):
    if s == "":
        return 0
    elif s[-1] == '#':
        return 1 + 2 * binary(s[:-1])
    else:
        return 2 * binary(s[:-1])

assert binary('...#...#.') == 34

class Map():
    def __init__(self, file):
        lines = [line.strip() for line in open('20/' + file).readlines()]
        self.algorithm = lines[0]
        self.map = list(map(list, lines[2:]))
        self.pad(['.'])

    def cell(self,x,y):
        if x<0 or x>=len(self.map[0]) or y<0 or y>=len(self.map):
            return self.map[0][0]
        else:
            return self.map[y][x]

    def pad(self, extendChar = None):
        # Pad the border with dark pixels to simulate being infinite map
        borderSize = 1 # Is sufficient width

        if extendChar is None:
            extendChar = [self.map[0][0]]

        # Top
        for _ in range(borderSize):
            self.map = [extendChar * len(self.map[0])] + self.map

        # Bottom
        for _ in range(borderSize):
            self.map.append(extendChar * len(self.map[0]))

        # Left
        for y in range(len(self.map)):
            self.map[y] = extendChar * borderSize + self.map[y]

        # Right
        for y in range(len(self.map)):
            self.map[y] = self.map[y] + extendChar * borderSize

    def enhance(self, num=1):
        for _ in range(num):
            newMap = copy.deepcopy(self.map)
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    pixels = ""
                    for v in [-1,0,1]:
                        for u in [-1,0,1]:
                            pixels += self.cell(x+u, y+v)
                    newMap[y][x] = self.algorithm[binary(pixels)]
            self.map = newMap
            self.pad()

    def numPixels(self):
        return len([c for line in self.map for c in line if c == '#'])

    def print(self):
        for line in self.map:
            print(''.join(line))
        print()
        
m = Map('test.txt')
m.enhance(2)
assert m.numPixels() == 35
m.enhance(48)
assert m.numPixels() == 3351

m = Map('input.txt')
m.enhance(2)
print(m.numPixels())
m.enhance(48)
print(m.numPixels())