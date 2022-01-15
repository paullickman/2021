class Amphipod():
    def __init__(self, file):
        self.grid = open('23/' + file).readlines()

    def __repr__(self):
        return ''.join(self.grid)

a = Amphipod('test.txt')
print(a)