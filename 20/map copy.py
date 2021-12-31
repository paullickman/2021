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
        self.pad()

    def pad(self):
        # Pad the border with dark pixels to simulate being infinite map
        borderSize = 10

        extendChar = self.map[0][0]

        # Top
        if any(['#' in line for y in range(borderSize) for line in self.map[y]]):
            for _ in range(borderSize):
                self.map = [['.'] * len(self.map[0])] + self.map

        # Bottom
        if any(['#' in line for y in range(borderSize) for line in self.map[-y-1]]):
            for _ in range(borderSize):
                self.map.append(['.'] * len(self.map[0]))

        # Left
        if any(['#' in line[:borderSize] for line in self.map]):
            for y in range(len(self.map)):
                self.map[y] = ['.'] * borderSize + self.map[y]

        # Right
        if any(['#' in line[-borderSize:] for line in self.map]):
            for y in range(len(self.map)):
                self.map[y] = self.map[y] + ['.'] * borderSize

    def enhance(self):
        newMap = copy.deepcopy(self.map)
        for y in range(1, len(self.map)-1):
            for x in range(1, len(self.map[0])-1):
                pixels = ''.join(self.map[y-1][x-1:x+2] + self.map[y][x-1:x+2] + self.map[y+1][x-1:x+2])
                newMap[y][x] = self.algorithm[binary(pixels)]
        self.map = newMap
        self.pad()

    def numPixels(self):
        return len([c for line in self.map for c in line if c == '#'])

    def print(self):
        for line in self.map:
            print(''.join(line))
        print()
        
# m = Map('test.txt')
# m.enhance()
# m.enhance()
# assert m.numPixels() == 35

m = Map('input.txt')
m.print()
m.enhance()
m.enhance()
m.print()

#6254 too high