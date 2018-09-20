"""
Bismuth Heavy3 Algorithm

Check test vectors
"""

import mmap
import os
import sys
import time
from hashlib import sha224

# custom modules
sys.path.append('../modules')
import annealing
import helpers
import vectors


# Run CSPRNG/test_create first
MAP = '../CSPRNG/rnd.bin'

if __name__ == '__main__':
    print("Checking nonce for Heavy3 Algorithm, block_hash={}".format(vectors.BLOCK_HASH))

    F = open(MAP, "rb+")
    # memory-map the file, size 0 means whole file
    MMAP = mmap.mmap(F.fileno(), 0)
    annealing.RND_LEN = os.path.getsize(MAP) // 4
    try:
        for nonce, diff in vectors.NONCES['heavy3'].items():
            start_time = time.time()
            real_diff = helpers.diffme_heavy3(MMAP, vectors.ADDRESS, nonce, vectors.BLOCK_HASH)
            end_time = time.time()
            print("Nonce {}: diff {} vs planned {}".format(nonce, real_diff, diff))
            print("Duration {} s".format(end_time - start_time))
            # already done in diffme, but recalc to print
            # Here, will need annealing twice
            # hash = sha224((vectors.ADDRESS + nonce + vectors.BLOCK_HASH).encode("utf-8")).hexdigest()
            # print(" Hash is {}".format(hash))
    finally:
        MMAP.close()
        F.close()


