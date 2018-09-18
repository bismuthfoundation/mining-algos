"""

"""

import mmap
import os
import sys

# custom modules
sys.path.append('../modules')
import annealing

# Run CSPRNG/test_create first
MAP = '../CSPRNG/rnd.bin'

# File len in 32 bits words.
RND_LEN = os.path.getsize(MAP) // 4


if __name__ == '__main__':
    F = open(MAP, "rb+")
    # memory-map the file, size 0 means whole file
    MMAP = mmap.mmap(F.fileno(), 0)
    annealing.RND_LEN = os.path.getsize(MAP) // 4
    try:
        test = annealing.anneal128_verbose(MMAP, 0xb2993d772ba10510000d39590cfe94a9)
        print(test)
    finally:
        MMAP.close()
        F.close()
