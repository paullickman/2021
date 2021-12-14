import re
import collections

class Polymer():
    def __init__(self, file):
        lines = open('14/'+file).read()
        self.template = lines.split('\n')[0]

        rules = re.findall(r'(\S+) -> (\S+)', lines)
        self.insertion = {}
        for a,b in rules:
            self.insertion[a] = b

        self.count = collections.defaultdict(int)
        for i in range(len(self.template)-1):
            pair = self.template[i:i+2]
            self.count[pair] += 1

    def iterate(self, n):
        for _ in range(n):
            newCount = collections.defaultdict(int)
            for k in list(self.count.keys()):
                if self.count[k] > 0:
                    insertChar = self.insertion[k]
                    pair1 = k[0]+insertChar
                    pair2 = insertChar+k[1]
                    newCount[pair1] += self.count[k]
                    newCount[pair2] += self.count[k]
            self.count = newCount

    def quantity(self):
        counter = collections.Counter()
        for k in self.count.keys():
            counter[k[0]] += self.count[k]
            counter[k[1]] += self.count[k]
        # Add start and end of template which are only counted once
        counter[self.template[0]] += 1
        counter[self.template[-1]] += 1
        mostCommonAmount = counter.most_common(1)[0][1]
        leastCommonAmount = counter.most_common()[-1][1]
        return (mostCommonAmount - leastCommonAmount) // 2 # Approach double counts

p = Polymer('test.txt')
p.iterate(10)
assert p.quantity() == 1588
p.iterate(30)
assert p.quantity() == 2188189693529

p = Polymer('input.txt')
p.iterate(10)
print(p.quantity())
p.iterate(30)
print(p.quantity())