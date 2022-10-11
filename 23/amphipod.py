import copy
import collections

# Energy used moving
score = {'A':1, 'B':10, 'C':100, 'D':1000}

amphipods = score.keys()
validCell = list(amphipods) + ['.']

# Room destination x-coord
destination = {3:'A', 5:'B', 7:'C', 9:'D'}

target = {}
for k in destination.keys():
    target[destination[k]] = k

def pathClear(grid, path):
    return all(grid[y][x] == '.' for x,y in path)

class Amphipod():
    def __init__(self, file):
        self.grid = list(map(lambda line: [c for c in line], open('23/' + file).readlines()))
        self.roomDepth = len(self.grid) - 3

        self.solvedStr = '...........'
        for c in "ABCD":
            self.solvedStr += c * self.roomDepth

        # Dictionary of pre-cached possible moves
        # moves[('A', (1,1))] = [((3,2), 2, [(2,1)]), ...]
        # Above means that an 'A' at (1,1) can move to (3,2) in 2 steps assuming path of [(2,1)] is clear
        self.moves = {}
        self.calcMoves()

    def gridString(self, g):
        s = ''.join(g[1][1:-2])
        for x in [3,5,7,9]:
            for y in range(self.roomDepth):
                s = s + g[y+2][x]
        return s

    def calcMoves(self):
        for y in range(1, len(self.grid)-1):
            for x in range(1, len(self.grid[y])-1):
                if self.grid[y][x] in validCell:
                    for amphipod in amphipods:
                        paths = self.calcPaths(amphipod, (x,y))
                        self.moves[(amphipod, (x,y))] = [(path[-1], (len(path) - 1) * score[amphipod], list(filter(lambda cell: cell[1] != 1 or (cell[0] not in destination.keys()), path[1:]))) for path in paths]

    def cells(self, path):
        # Possible next moves
        moves = []
        for i,j in [(-1,0), (1,0), (0,-1), (0,1)]:
            x = path[-1][0] + i
            y = path[-1][1] + j
            if self.grid[y][x] in validCell and (x,y) not in path:
                moves.append((x,y))
        return moves

    def calcPaths(self, ampithod, start):
        paths = []
        frontier = [[start]]
        while frontier:
            newFrontier = []
            for path in frontier:
                for cell in self.cells(path):
                    newFrontier.append(path + [cell])
            paths.extend(newFrontier)
            frontier = newFrontier

        # Ensure paths don't stop in front of a room
        paths = list(filter(lambda path: not(path[-1][1] == 1 and path[-1][0] in destination.keys()), paths))

        # Ensure that if the path started in hallway then it doesn't finish in the hallway
        paths = list(filter(lambda path: not(path[0][1] == 1 and path[-1][1] == 1), paths))

        # Ensure that if the path finishes in a room, then it is the right amphipod
        paths = list(filter(lambda path: not(path[-1][1] > 1 and ampithod != destination[path[-1][0]]), paths))

        # Ensure that the right amphipod doesn't leave bottom row of room
        paths = list(filter(lambda path: not(path[0][1] == self.roomDepth+1 and ampithod == destination[path[0][0]]), paths))

        return paths

    def __repr__(self):
        return ''.join(map(lambda line: ''.join(line), self.grid))

    def leastEnergy(self):

        gridStr = self.gridString(self.grid)

        minEnergy = collections.defaultdict(lambda: (1000000, None)) # Infinity
        minEnergy[gridStr] = (0, self.grid)

        remaining = set([gridStr])

        while remaining:
            gridStr = min([k for k in remaining], key=lambda k: minEnergy[k][0]) # PRL Improve efficiency
            remaining.remove(gridStr)

            energy, grid = minEnergy[gridStr]

            if gridStr == self.solvedStr:
                return energy

            for y in range(1, len(grid)):
                for x in range(1, len(grid[y])):
                    if grid[y][x] in amphipods:
                        amphipod = grid[y][x]

                        moves = []
                        for dest, energyIncr, path in self.moves[(amphipod, (x,y))]:
                            if pathClear(grid, path):

                                # Check that right ampithod only leaves a room if wrong ampithod in a lower room
                                if y>1 and y<self.roomDepth+1 and amphipod == destination[x]:
                                    if any(grid[j][x] == amphipod for j in range(y+1, self.roomDepth+2)):
                                        continue

                                # Ensure that right ampithod doesn't stop at a room if a lower room is empty
                                if dest[1]>1 and dest[1]<self.roomDepth+1 and amphipod == destination[dest[0]]:
                                    if any(grid[j][dest[0]] == '.' for j in range(dest[1]+1, self.roomDepth+2)):
                                        continue

                                # Ensure that right amphipod doesn't stop at top room if bottom room has wrong amphipod
                                if dest[1]>1 and dest[1]<self.roomDepth+1 and amphipod == destination[dest[0]]:
                                    if any(grid[j][dest[0]] != amphipod for j in range(dest[1]+1, self.roomDepth+2)):
                                        continue

                                newEnergy = energy + energyIncr

                                newGrid = copy.deepcopy(grid)
                                newGrid[y][x] = '.'
                                newGrid[dest[1]][dest[0]] = amphipod

                                newGridStr = self.gridString(newGrid)

                                if newEnergy < minEnergy[newGridStr][0]:
                                    minEnergy[newGridStr] = (newEnergy, newGrid)
                                    remaining.add(newGridStr)

a = Amphipod('test.txt')
assert a.leastEnergy() == 12521

a = Amphipod('test2.txt')
assert a.leastEnergy() == 44169

a = Amphipod('input.txt')
print(a.leastEnergy())

a = Amphipod('input2.txt')
print(a.leastEnergy())