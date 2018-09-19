"""
Bismuth Heavy2

SHA State Annealing
"""

import mmap
import os
import sys

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
    try:
        test = annealing.anneal224_verbose(MMAP, 0x7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1)
        print("old", test)
        test = annealing.anneal_hash_verbose(MMAP, 0x7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1)
        print("new", test)
    finally:
        MMAP.close()
        F.close()

    """
    n 5e3958a1
    i 0e3958a1
    v 672fbc15
    n d8ee1042
    i 08ee1042
    v 708337e4
    n 971ede0e
    i 071ede0e
    v f25f6ed8
    n 22a87f8b
    i 02a87f8b
    v ebc84a81
    n 1adbde86
    i 0adbde86
    v 45c5ed3c
    n 76aca387
    i 06aca387
    v 7982527a
    n 7a0f3848
    i 0a0f3848
    v bd2ba316
    old 672fbc15708337e4f25f6ed8ebc84a8145c5ed3c7982527abd2ba316
    n 5e3958a1
    i 0e3958a1
    v 672fbc15
    n d8ee1042
    i 08ee1042
    v 708337e4
    n 971ede0e
    i 071ede0e
    v f25f6ed8
    n 22a87f8b
    i 02a87f8b
    v ebc84a81
    n 1adbde86
    i 0adbde86
    v 45c5ed3c
    n 76aca387
    i 06aca387
    v 7982527a
    n 7a0f3848
    i 0a0f3848
    v bd2ba316
    new bd2ba3167982527a45c5ed3cebc84a81f25f6ed8708337e4672fbc15

    """
