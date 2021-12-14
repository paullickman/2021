import collections

def allowed(node, history, visits):
    if not node.islower():
        return True
    elif node in ['start', 'end']:
        return not (node in history)
    else:
        count = len([node for h in history if node==h])
        if count == 0:
            return True
        if visits == 2 and count == 1:
            others = collections.Counter([h for h in history if h.islower()])
            if [o for o in others if others[o] > 1]:
                return False
            return True
        return False

class Passage():
    def __init__(self, file):
        self.passages = collections.defaultdict(list)
        for line in open('12/'+file).readlines():
            src, dest = line.strip().split('-')
            self.passages[src].append(dest)
            self.passages[dest].append(src)

    def pathSearch(self, node, history, visits):
        if node == 'end':
            return [history]
        pathsList = []
        for nextNode in self.passages[node]:
            if allowed(nextNode, history, visits):
                pathsList.extend(self.pathSearch(nextNode, history + [nextNode], visits))
        return pathsList
                
    def paths(self, node, visits):
        return self.pathSearch(node, [node], visits)

    def numPaths(self, visits = 1):
        return len(self.paths('start', visits))

p = Passage('test1.txt')
assert p.numPaths() == 10

p = Passage('test2.txt')
assert p.numPaths() == 19

p = Passage('test3.txt')
assert p.numPaths() == 226

p = Passage('input.txt')
print(p.numPaths())

p = Passage('test1.txt')
assert p.numPaths(2) == 36

p = Passage('test2.txt')
assert p.numPaths(2) == 103

p = Passage('test3.txt')
assert p.numPaths(2) == 3509

p = Passage('input.txt')
print(p.numPaths(2))
