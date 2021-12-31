class Cavern:
    def __init__(self,file):
        cave = open('15/' + file).readlines()
        self.cave = list(map(lambda line: list(map(int, line.strip())), cave))
        self.height = len(self.cave)
        self.width = len(self.cave[0])

    def neighbours(self, c):
        nList = []
        for i,j in [(-1,0),(1,0),(0,-1),(0,1)]:
            u,v = c[0]+i,c[1]+j
            if u>=0 and v>=0 and u<self.width and v<self.height:
                nList.append((u,v))
        return nList

    def risk(self):
        risks = [[None] * self.width for _ in range(self.height)]

        start = (0,0)
        
        risks[start[1]][start[0]] = 0

        frontier = set([start])
        while frontier:
            newFrontier = set()
            for f in frontier:
                for n in self.neighbours(f):
                    if (risks[n[1]][n[0]] is None) or (risks[f[1]][f[0]] + self.cave[n[1]][n[0]] < risks[n[1]][n[0]]):
                        risks[n[1]][n[0]] = risks[f[1]][f[0]] + self.cave[n[1]][n[0]]
                        newFrontier.add(n)
            frontier = newFrontier
        return risks[self.height-1][self.width-1]

    def extend(self):
        height = self.height * 5
        width = self.width * 5
        cave = [[None] * width for _ in range(height)]

        for j in range(height):
            for i in range(width):
                if j < self.height:
                    if i < self.width:
                        cave[j][i] = self.cave[j][i]
                    else:
                        cave[j][i] = cave[j][i-self.width] % 9 + 1
                else:
                    cave[j][i] = cave[j-self.height][i] % 9 + 1

        self.cave = cave
        self.height = height
        self.width = width

c = Cavern('test.txt')
assert c.risk() == 40
c.extend()
assert c.risk() == 315

c = Cavern('input.txt')
print(c.risk())
c.extend()
print(c.risk())
