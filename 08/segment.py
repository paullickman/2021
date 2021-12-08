import re
import itertools

# Segments required for each digit 0,1,2...
digits = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
digitsSorted = sorted(digits)

def transform(perm, signal):
    return [''.join(sorted(map(lambda c: perm[ord(c) - ord('a')], s))) for s in signal]

assert transform('bcda', ['abcd', 'cd']) == ['abcd', 'ad']
                
def solution(perm, signal):
    signal = sorted(transform(perm, signal))
    return signal == digitsSorted

def solve(line):
    signal = line[0]
    output = line[1]
    for perm in itertools.permutations('abcdefg'):
        if solution(perm, signal):
            return int(''.join([str(digits.index(n)) for n in transform(perm, output)]))
        
    return None

class Segment():
    def __init__(self, file):
        self.notes = []
        for line in open('08/'+file).readlines():
            words = re.findall(r'\S+', line)
            self.notes.append((words[:10],words[11:]))

    def count1478(self):
        return len([s for note in self.notes for s in note[1] if len(s) in [2,4,3,7]])

    def sum(self):
        return sum(map(solve, self.notes))
    
s = Segment('test.txt')
assert s.count1478() == 26
assert s.sum() == 61229

s = Segment('input.txt')
print(s.count1478())            
print(s.sum())
