import re

class Origami:
    def __init__(self, file):
        lines = open('13/'+file).read()
        
        dots = re.findall(r'(\d+),(\d+)', lines)
        self.dots = set((int(x),int(y)) for x,y in dots)

        folds = re.findall(r'(\S+)=(\S+)', lines)
        self.folds = [(a,int(n)) for a,n in folds]

    def fold(self,num):
        axis, value = self.folds[num]
        if axis == 'x':
            for dot in list(self.dots):
                if dot[0] > value:
                    self.dots.add((value*2-dot[0],dot[1]))
                    self.dots.remove(dot)
        else:
            for dot in list(self.dots):
                if dot[1] > value:
                    self.dots.add((dot[0],value*2-dot[1]))
                    self.dots.remove(dot)

    def numDots(self):
        return len(self.dots)

    def allFolds(self):
        for i in range(len(self.folds)):
            self.fold(i)

    def print(self):
        maxX = max([x for x,_ in self.dots])
        maxY = max([y for _,y in self.dots])
        for j in range(maxY+1):
            for i in range(maxX+1):
                if (i,j) in self.dots:
                    print('#', end='')
                else:
                    print(' ', end='')
            print()
                    
o = Origami('test.txt')
o.fold(0)
assert o.numDots() == 17

o = Origami('input.txt')
o.fold(0)
print(o.numDots())

o = Origami('input.txt')
o.allFolds()
o.print()
