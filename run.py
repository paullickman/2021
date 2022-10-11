# Run all days

import glob
import runpy
import time

print ('Answers')

day = 1
times = []
while True:
    g = glob.glob(('0' if day < 10 else '') + str(day) + '/*.py')
    if g == []:
        break
    start = time.time()
    print('Day', day)
    runpy.run_path(g[0])
    elapsed = int(time.time() - start)
    times.append(elapsed)
    print()
    day += 1

print('Times')

maxTime = max(times)
for day in range(len(times)):
    print('Day', day+1, ' : ', "*" * int(times[day]/maxTime*30))