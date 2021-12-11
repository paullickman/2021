import re

class Octopus:
    def __init__(self, file):
        self.grid = []
        for line in open('11/'+file).readlines():
            self.grid.append([int(n) for n in re.findall(r'(\d)', line)])
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def neighbours(self,x,y):
        locations = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not(i==0 and j==0):
                    u,v = x+i,y+j
                    if u>=0 and u<self.width and v>=0 and v<self.height:
                        locations.append((u,v))
        return locations

    def step(self):

        for i in range(self.width):
            for j in range(self.height):
                self.grid[j][i] += 1
        
        numFlashes = 0
        newFlash = True
        while newFlash:
            newFlash = False
            for i in range(self.width):
                for j in range(self.height):
                    if self.grid[j][i] > 9:
                        self.grid[j][i] = 0
                        numFlashes += 1
                        newFlash = True
                        for u,v in self.neighbours(i,j):
                            if self.grid[v][u] != 0:
                                self.grid[v][u] += 1
            
        return numFlashes

    def flashes(self, steps):
        num = 0
        for _ in range(steps):
            num += self.step()
        return num

    def blank(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[j][i]:
                    return False
        return True        

    def synchronise(self):
        step = 0
        while not self.blank():
            self.step()
            step += 1
        return step
 
s = Octopus('test.txt')          
assert s.flashes(100) == 1656
s = Octopus('test.txt')          
assert s.synchronise() == 195

s = Octopus('input.txt')          
print(s.flashes(100))
s = Octopus('input.txt')          
print(s.synchronise())
