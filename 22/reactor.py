import re
from collections import namedtuple

Point = namedtuple('Point', 'x y z')

class Cuboid():
    def __init__(self, minX, maxX, minY, maxY, minZ, maxZ):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.minZ = minZ
        self.maxZ = maxZ

    def __repr__(self):
        return 'x=%s..%s,y=%s..%s,z=%s..%s' % (self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)

    def cubes(self):
        return (self.maxX - self.minX + 1) * (self.maxY - self.minY + 1) * (self.maxZ - self.minZ + 1)

class Step(Cuboid):
    def __init__(self, switch, minX, maxX, minY, maxY, minZ, maxZ):
        self.switch = switch
        super().__init__(minX, maxX, minY, maxY, minZ, maxZ)

# Determined whether a point is within a cuboid
def contained(p, c):
    return p.x >= c.minX and p.x <= c.maxX and p.y >= c.minY and p.y <= c.maxY and p.z >= c.minZ and p.z <= c.maxZ

# Calculates the points of a steps' vertices
def vertices(s):
    v = []
    for x in [s.minX, s.maxX]:
        for y in [s.minY, s.maxY]:
            for z in [s.minZ, s.maxZ]:
                v.append(Point(x,y,z))
    return v

# Determine how a 1d line can be chunked up by intersection
def regions(x,y, u,v):
    if y<u or v<x:
        # No interserction
        return[(x,y)]
    elif u<=x:
        if v<y:
            return [(x,v), (v+1,y)]
        else:
            return [(x,y)]
    else:
        if y<=v:
            return [(x,u-1), (u,y)]
        else:
            return [(x,u-1), (u,v), (v+1,y)]

class Reactor():

    def process(self, step):
        # Want to add parts of each cuboid which don't overlap with step
        # Construct 3x3x3 mega cuboid and test each sub-cuboid
        newCuboids = []
        for c in self.cuboids:
            for x1,x2 in regions(c.minX, c.maxX, step.minX, step.maxX):
                for y1,y2 in regions(c.minY, c.maxY, step.minY, step.maxY):
                    for z1,z2 in regions(c.minZ, c.maxZ, step.minZ, step.maxZ):
                        subCuboid = Cuboid(x1, x2, y1, y2, z1, z2)
                        #print('Checking:', subCuboid)
                        # Check that subCuboid is wholly within cuboid and wholly outside of step
                        if all([contained(p,c) for p in vertices(subCuboid)]) and not(any([contained(p,step) for p in vertices(subCuboid)])):
                            newCuboids.append(subCuboid)
        self.cuboids = newCuboids
        #print(newCuboids)

    def __init__(self, file, limit=None):
        # Non-overlapping list of cuboids
        self.cuboids = []
        self.steps = []
        for line in open('22/' + file).readlines():
            step = re.findall(r'^\S+|-?\d+', line)
            step = Step(step[0], int(step[1]), int(step[2]), int(step[3]), int(step[4]), int(step[5]), int(step[6]))
            if (limit is None) or all([abs(n) <= limit for n in [step.minX, step.maxX, step.minY, step.maxY, step.minZ, step.maxZ]]):
                self.steps.append(step)

        # Construct list of cuboids
        for step in self.steps:
            print('Step:', step)
            self.process(step)
            if step.switch == 'on':
                self.cuboids.append(Cuboid(step.minX, step.maxX, step.minY, step.maxY, step.minZ, step.maxZ))
            print('Num cuboids:', len(self.cuboids))
            #print('Cuboids:', self.cuboids)

    def cubes(self):
        return sum([c.cubes() for c in self.cuboids])

r = Reactor('test1.txt', 50)
assert r.cubes() == 39

r = Reactor('test2.txt', 50)
assert r.cubes() == 590784

r = Reactor('input.txt', 50)
print(r.cubes())

r = Reactor('test3.txt')
assert r.cubes() == 2758514936282235

r = Reactor('input.txt')
print(r.cubes())

# PRL Make faster