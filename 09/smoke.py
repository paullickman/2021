import re

class Smoke:
    def __init__(self, file):
        self.map = []
        for line in open('09/'+file).readlines():
            self.map.append([int(n) for n in re.findall(r'(\d)', line)])
        self.height = len(self.map)
        self.width = len(self.map[0])

    def neighbours(self,x,y):
        locations = []
        for i,j in [(-1,0),(1,0),(0,-1),(0,1)]:
            u,v = x+i,y+j
            if u>=0 and u<self.width and v>=0 and v<self.height:
                locations.append((u,v))
        return locations

    def low(self,x,y):
        for u,v in self.neighbours(x,y):
            if self.map[y][x] >= self.map[v][u]:
                return False
        return True

    def risk(self,x,y):
        return 1 +  self.map[y][x]

    def count(self):
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.low(x,y):
                    total += self.risk(x,y)
        return total

    def size(self,x,y):
        basin = [(x,y)]
        frontier = [(x,y)]
        while len(frontier) > 0:
            newFrontier = []
            for f in frontier:
                for location in self.neighbours(f[0],f[1]):
                    if location not in basin and location not in newFrontier:
                        if self.map[f[1]][f[0]] < self.map[location[1]][location[0]] and self.map[location[1]][location[0]] != 9:
                            newFrontier.append(location)
            basin.extend(newFrontier)
            frontier = newFrontier
        return len(basin)
        

    def basins(self):
        sizes = []
        for y in range(self.height):
            for x in range(self.width):
                if self.low(x,y):
                    sizes.append(self.size(x,y))
        sizes.sort(reverse=True)
        return sizes[0]*sizes[1]*sizes[2]
 
s = Smoke('test.txt')            
assert s.count() == 15
assert s.basins() == 1134

s = Smoke('input.txt')            
print(s.count())
print(s.basins())

