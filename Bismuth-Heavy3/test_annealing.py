"""
Bismuth Heavy3

SHA State Annealing
"""

import mmap
import os
import sys
import time

# custom modules
sys.path.append('../modules')
import annealing

# Run CSPRNG/test_create first
MAP = '../CSPRNG/rnd.bin'


if __name__ == '__main__':
    F = open(MAP, "rb+")
    # memory-map the file, size 0 means whole file
    MMAP = mmap.mmap(F.fileno(), 0)
    annealing.RND_LEN = os.path.getsize(MAP) // 4
    print("RND_LEN", annealing.RND_LEN)
    try:
        start_time = time.time()
        test = annealing.anneal3_verbose(MMAP, 0x7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1)
        # test = annealing.anneal3(MMAP, 0x7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1)
        end_time = time.time()
        print("Annealed", test)
        print("duration {} sec".format(end_time - start_time))
    finally:
        MMAP.close()
        F.close()

"""
RND_LEN 268435456
n 7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1
h7 5e3958a1
index 0e3958a0
F7 82675626
v7 dc5e0e87
h d8ee1042
index 0e3958a1
v e1f8f4f6
h 971ede0e
index 0e3958a2
v 43c1815e
h 22a87f8b
index 0e3958a3
v aac2533e
h 1adbde86
index 0e3958a4
v 04100269
h 76aca387
index 0e3958a5
v 5cdf502d
h 7a0f3848
index 0e3958a6
v ede9b329
Annealed ede9b3295cdf502d04100269aac2533e43c1815ee1f8f4f6dc5e0e87
"""
