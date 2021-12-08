class Fish:
    def __init__(self, file):
        self.fish = list(map(int, open('06/'+file).read().split(',')))

    def iterate(self, n=1):
        for _ in range(n):
            self.fish = list(map(lambda x: 6 if x==0 else x-1, self.fish)) + [8 for x in self.fish if x==0]
    
f = Fish('test.txt')
f.iterate(80)
assert len(f.fish) == 5934

f = Fish('input.txt')
f.iterate(80)
print(len(f.fish))

class FishFast:
    def __init__(self, file):
        self.counts = [0] * 9 # 9 different values 
        fish = list(map(int, open('06/'+file).read().split(',')))
        for f in fish:
            self.counts[f] += 1

    def iterate(self, n=1):
        for _ in range(n):
            self.counts = self.counts[1:7] + [self.counts[0]+self.counts[7], self.counts[8], self.counts[0]]

    def count(self):
        return sum(self.counts)

f = FishFast('test.txt')
f.iterate(256)
assert f.count() == 26984457539

f = FishFast('input.txt')
f.iterate(256)
print(f.count())
