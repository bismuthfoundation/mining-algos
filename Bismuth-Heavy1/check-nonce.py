"""
Bismuth Legacy Algorithm

Check test vectors
"""

import mmap
import os
import sys
from hashlib import sha224

# custom modules
sys.path.append('../modules')
import annealing
import helpers
import vectors


# Run CSPRNG/test_create first
MAP = '../CSPRNG/rnd.bin'

if __name__ == '__main__':
    print("Checking nonce for Heavy1 Algorithm, block_hash={}".format(vectors.BLOCK_HASH))

    F = open(MAP, "rb+")
    # memory-map the file, size 0 means whole file
    MMAP = mmap.mmap(F.fileno(), 0)
    annealing.RND_LEN = os.path.getsize(MAP) // 4
    try:
        for nonce, diff in vectors.NONCES['heavy1'].items():
            real_diff = helpers.diffme_heavy1_full(MMAP, vectors.ADDRESS, nonce, vectors.BLOCK_HASH)
            print("Nonce {}: diff {} vs planned {}".format(nonce, real_diff, diff))
            # already done in diffme, but recalc to print
            # Here, will need annealing twice
            # hash = sha224((vectors.ADDRESS + nonce + vectors.BLOCK_HASH).encode("utf-8")).hexdigest()
            # print(" Hash is {}".format(hash))
    finally:
        MMAP.close()
        F.close()

"""
nonce 4a94ef265a682330e9d0d331aca248bc
a_nonce d1281076b702f2b01ea0d38b064296e9
a_sha c651dda16449d7bc8f4f31b265e97a0f3890762cc7b491db7edc0a2e
"""

