import re

class Shot():
    def __init__(self, file):
        nums = re.findall(r'-?\d+', open('17/' + file).read())
        self.targetXLow = int(nums[0])
        self.targetXHigh = int(nums[1])
        self.targetYLow = int(nums[2])
        self.targetYHigh = int(nums[3])

    def shoot(self, velocityX, velocityY):
        x,y = 0,0
        maxY = y
        while x<=self.targetXHigh and y>=self.targetYLow:
            if x>= self.targetXLow and x<=self.targetXHigh and y<=self.targetYHigh and y>=self.targetYLow:
                return (True, maxY)
            x += velocityX
            y += velocityY
            if y>=maxY:
                maxY = y
            if velocityX>=1:
                velocityX -= 1
            elif velocityX<=-1:
                velocityX += 1
            velocityY -= 1
        return (False,)

    def highest(self):
        maxY = None
        self.count = 0
        for velocityX in range(-400,400): # PRL not hardcoded!!!
            for velocityY in range(-400,400):
                s = self.shoot(velocityX, velocityY)
                if s[0]:
                    self.count += 1
                    if maxY == None or s[1]>maxY:
                        maxY = s[1]
        return maxY

s = Shot('test.txt')
assert s.shoot(7,2)[0] == True
assert s.shoot(6,3)[0] == True
assert s.shoot(9,0)[0] == True
assert s.shoot(17,-4)[0] == False

assert s.highest() == 45
assert s.count == 112

s = Shot('input.txt')
print(s.highest())
print(s.count)
