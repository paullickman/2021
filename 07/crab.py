class Crab:
    def __init__(self, file):
        self.positions = list(map(int, open('07/'+file).read().split(',')))

    def fuel(self, pos):
        return sum([abs(pos-p) for p in self.positions])

    def fuel2(self, pos):
        return sum([abs(pos-p)*(abs(pos-p)+1)//2 for p in self.positions])

    def align(self, f=fuel):
        return min(f(self,pos) for pos in range(min(self.positions), max(self.positions)+1))

c = Crab('test.txt')
assert c.align() == 37
assert c.align(Crab.fuel2) == 168

c = Crab('input.txt')
print(c.align())
print(c.align(Crab.fuel2))
