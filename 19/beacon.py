import re

def rotX(b):
    return list(map(lambda p: (p[0],p[2],-p[1]), b))
def rotY(b):
    return list(map(lambda p: (-p[2],p[1],p[0]), b))
def rotZ(b):
    return list(map(lambda p: (p[1],-p[0],p[2]), b))

def overlaps(s1, s2):
    maxOverlaps = 0
    overlapPos = None
    for p1 in s1:
        for p2 in s2:
            offset = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])
            shift = [(q[0] + offset[0], q[1] + offset[1], q[2] + offset[2]) for q in s2]
            numOverlaps = len([o for o in s1 if o in shift]) # Not using 1000 limit
            if numOverlaps >= 12:
                return offset
    return None

class Scanner():
    def __init__(self, file):
        lines = [line.strip() for line in open('19/' +  file).readlines()]

        self.scanners = []
        beacons = []

        for line in lines:
            parse = (re.findall(r'(-?\d+)', line))

            if len(parse) < 3:
                if len(beacons) > 0:
                    self.scanners.append([beacons])
                    beacons = []
            else:
                beacons.append((int(parse[0]), int(parse[1]), int(parse[2])))

        if len(beacons) > 0:
            self.scanners.append([beacons])

        # Add rotations

        i = 1 # Don't rotate scanner 0
        while i < len(self.scanners):
            beacons = self.scanners[i][0]

            for _ in range(3):
                beacons = rotZ(beacons)
                self.scanners[i].append(beacons)

            beacons = rotZ(beacons)
            beacons = rotX(beacons)

            for _ in range(4):
                for _ in range(4):
                    beacons = rotZ(beacons)
                    self.scanners[i].append(beacons)
                beacons = rotY(beacons)

            beacons = rotX(beacons)

            for _ in range(4):
                beacons = rotZ(beacons)
                self.scanners[i].append(beacons)

            i += 1

        # Calculate scanner positions

        self.scannerPosition = [None] * len(self.scanners)
        self.scannerRotation = [None] * len(self.scanners)

        self.scannerPosition[0] = (0,0,0)
        self.scannerRotation[0] = 0

        while any(x is None for x in self.scannerPosition):
            for i in range(len(self.scanners)):
                if self.scannerPosition[i] is None:
                    for scanner in range(len(self.scanners)):
                        if self.scannerPosition[scanner] is not None:
                            for rot in range(24):
                                offset = overlaps(self.scanners[scanner][self.scannerRotation[scanner]], self.scanners[i][rot])
                                if offset is not None:
                                    self.scannerPosition[i] = (self.scannerPosition[scanner][0] + offset[0], self.scannerPosition[scanner][1] + offset[1], self.scannerPosition[scanner][2] + offset[2])
                                    self.scannerRotation[i] = rot

    def numBeacons(self):
        beacons = set()
        for i in range(len(self.scanners)):
            for b in self.scanners[i][self.scannerRotation[i]]:
                beacons.add((self.scannerPosition[i][0]+b[0], self.scannerPosition[i][1]+b[1], self.scannerPosition[i][2]+b[2]))
        return len(beacons)

    def maxDistance(self):
        return max([abs(s1[0]-s2[0]) + abs(s1[1]-s2[1]) + abs(s1[2]-s2[2]) for s1 in self.scannerPosition for s2 in self.scannerPosition]) 

s = Scanner('test.txt')
assert s.numBeacons() == 79
assert s.maxDistance()== 3621

s = Scanner('input.txt')
print(s.numBeacons())
print(s.maxDistance())

# PRL Optimise - connect scanners that have been positioned yet?