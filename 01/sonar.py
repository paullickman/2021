class Depths:
    def __init__(self, file):
        f = open('01/'+file)
        self.nums = list(map(int, f.readlines()))

    def numIncr(self, diff = 1):
        total = 0
        i = 1
        while i <= len(self.nums)-diff:
            if self.nums[i-1] < self.nums[i+diff-1]:
                total += 1
            i += 1
        return total

d = Depths('test.txt')
assert d.numIncr() == 7
assert d.numIncr(3) == 5

d = Depths('input.txt')
print(d.numIncr())
print(d.numIncr(3))
