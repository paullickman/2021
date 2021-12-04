class Binary:
    def __init__(self, file):
        self.nums = list(map(lambda x: x.strip(), open('03/'+file).readlines()))

        self.counts = [0] * len(self.nums[0])

        for n in self.nums:
            for i in range(len(n)):
                if n[i] == '0':
                    self.counts[i] += 1

    def gamma(self):
        b = ''
        for c in self.counts:
            if c > len(self.nums) - c:
                b += '0'
            else:
                b += '1'
        return int(b, 2)
                    
    def epsilon(self):
        b = ''
        for c in self.counts:
            if c < len(self.nums) - c:
                b += '0'
            else:
                b += '1'
        return int(b, 2)

    def power(self):
        return self.gamma() * self.epsilon()

    def oxygen(self):
        nums = self.nums[:]
        i = 0
        while len(nums) > 1:
            count = 0
            for n in nums:
                if n[i] == '0':
                    count += 1
            if count > len(nums) - count:
                common = '0'
            else:
                common = '1'

            nums = [n for n in nums if n[i] == common]
            i += 1
            
        return int(nums[0], 2)

    def co2(self):
        nums = self.nums[:]
        i = 0
        while len(nums) > 1:
            count = 0
            for n in nums:
                if n[i] == '0':
                    count += 1
            if count <= len(nums) - count:
                common = '0'
            else:
                common = '1'

            nums = [n for n in nums if n[i] == common]
            i += 1
            
        return int(nums[0], 2)


    def life(self):
        return self.oxygen() * self.co2()

b = Binary('test.txt')
assert b.gamma() == 22
assert b.epsilon() == 9
assert b.power() == 198

assert b.oxygen() == 23
assert b.co2() == 10
assert b.life() == 230

b = Binary('input.txt')
print(b.power())
print(b.life())
