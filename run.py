# Run all days

import glob
import runpy

day = 1
while True:
    g = glob.glob(('0' if day < 10 else '') + str(day) + '/*.py')
    if g == []:
        break
    print('Day', day)
    runpy.run_path(g[0])
    print()
    day += 1
