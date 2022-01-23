import itertools

line5nums = [1,1,1,26,26,1,26,26,1,1,26,1,26,26]
line6nums = [12,13,13,-2,-10,13,-14,-5,15,15,-14,10,-14,-5]
line16nums = [7,8,10,4,4,6,11,13,1,8,4,13,4,14]

# PRL Change to process input.txt file as opposed to hard code the operations here

def f(i, z, w):
    x = 0
    y = 0

    x = x * 0
    x = x + z
    x = x % 26
    z = z // line5nums[i]
    x = x + line6nums[i]
    if x == w:
        x = 1
    else:
        x = 0
    if x == 0:
        x = 1
    else:
        x = 0
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + line16nums[i]
    y = y * x
    z = z + y

    return z

values = set([0])

for i in range(13,-1,-1):
    newValues = set()
    newSolution = []
    for initZ, initW in [(z,w) for z in range(-10000,10000) for w in range(1,10)]:
        z = f(i, initZ, initW)

        if z in values:
            newValues.add(initZ)

            if i == 13:
                newSolution.append((initZ, [initW]))
            else:
                for nextZ, nextW in solution:
                    if z == nextZ:
                        newSolution.append((initZ, [initW] + nextW))

    values = newValues
    solution = newSolution

m = max([w for z,w in solution if z == 0])
print(''.join(map(str, m)))

m = min([w for z,w in solution if z == 0])
print(''.join(map(str, m)))