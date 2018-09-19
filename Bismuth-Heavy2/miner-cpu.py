"""
Demo cpu miner for Bismuth Heavy 2 Algorithm

"""

import mmap
import os
import random
import struct
import sys
import time
from multiprocessing import Process
from hashlib import sha224

# custom modules
sys.path.append('../modules')
import helpers
import vectors
import annealing


__version__ = '0.0.1'

NONCE_COUNT = 1000

# To get reproducible results
SEED = 'Bismuth_Heavy_2'

THREAD_COUNT = 1

# A very low diff target for CPU tests
DIFF = 50

# How long to mine (sec)?
TIMEOUT = 600

# Run CSPRNG/test_create first
MAP = '../CSPRNG/rnd.bin'


def miner(q, address, db_block_hash, diff, mining_condition):
    tries = 0
    # One reproducible seed per thread
    random.seed(SEED + str(q))
    timeout = time.time() + TIMEOUT
    t1 = time.time()
    # temp = dict()
    while t1 < timeout:
        try:
            tries = tries + 1
            nonce_array = ["{:032x}".format(random.getrandbits(128)) for i in range(NONCE_COUNT)]
            possibles = [nonce for nonce in nonce_array if
                         mining_condition in (
                             annealing.anneal_hash(MMAP, int.from_bytes(
                                 sha224((address + nonce + db_block_hash).encode("utf-8")).digest(), 'big')))]
            # hash rate calculation
            try:
                t2 = time.time()
                khs = int((NONCE_COUNT / (t2 - t1)) / 1000)
            except Exception as e:
                khs = 1
            if possibles:
                for nonce in possibles:
                    real_diff = helpers.diffme_heavy2(MMAP, address, nonce, db_block_hash)
                    if real_diff <= diff:
                        pass
                        # print("Real diff {}".format(real_diff))
                    else:
                        print("{}: Nonce {} - real diff {} - {} kh/s - {} tries".format(q, nonce, real_diff, khs, tries))
                        # temp[nonce] = real_diff
            t1 = time.time()
        except Exception as e:
            print(e)
    # print(temp)


if __name__ == '__main__':
    F = open(MAP, "rb+")
    # memory-map the file, size 0 means whole file
    # File len in 32 bits words.
    annealing.RND_LEN = os.path.getsize(MAP) // 4
    MMAP = mmap.mmap(F.fileno(), 0)
    try:
        instances = range(THREAD_COUNT)
        # For reproducible tests
        random.seed(SEED)
        mining_condition_bin = helpers.bin_convert_orig(vectors.BLOCK_HASH)[:DIFF]
        diff_hex = int((DIFF / 8) - 1)
        mining_condition = vectors.BLOCK_HASH[:diff_hex]
        processes = []
        for q in instances:
            p = Process(target=miner, args=(
            str(q + 1), vectors.ADDRESS, vectors.BLOCK_HASH, DIFF, mining_condition))
            p.daemon = True
            p.start()
            processes.append(p)
        print("{} miners searching for solutions at difficulty {} and condition {}"
              .format(THREAD_COUNT, DIFF, mining_condition))
        for q in instances:
            processes[q].join()
            processes[q].terminate()
    finally:
        MMAP.close()
        F.close()


"""
nonce 1000, 600 sec, diff 50
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce fe29e15dcc7c65e05a3bd3cafc20ea9d - real diff 52 - 53 kh/s - 565 tries
1: Nonce abcfd68fa8ce06a6889b6a6514efb45e - real diff 53 - 51 kh/s - 805 tries
1: Nonce c60c26ea06aa3419fdee722e9a37dd3b - real diff 54 - 52 kh/s - 872 tries
1: Nonce c35eb5707cd5465edf07beda747b2394 - real diff 54 - 49 kh/s - 957 tries
1: Nonce 3a4df9b4ae1e3ec6cb6f377ce57ba72b - real diff 53 - 52 kh/s - 1421 tries
1: Nonce 4c1cfba931716d80e32404d985cd4717 - real diff 52 - 53 kh/s - 1992 tries
1: Nonce dcf3452b89d48cbd32bc1eb05044a3a2 - real diff 52 - 53 kh/s - 2442 tries
1: Nonce 2eadfddb3e959c9709342b77a29e2d82 - real diff 54 - 55 kh/s - 4794 tries
1: Nonce 0c03c050b8bc270f7af0d779ce26d1b1 - real diff 53 - 43 kh/s - 4801 tries
1: Nonce 856de8919191918952949b5f0eeaaf18 - real diff 53 - 53 kh/s - 5204 tries
1: Nonce 735de24cf32f7d91258c9bf958f96aa1 - real diff 53 - 54 kh/s - 8203 tries
1: Nonce e7bbe22a02a7d88302bd81b9440ffd11 - real diff 54 - 51 kh/s - 10117 tries
1: Nonce e13e1ad0ac35c3609bd3aaf39891e1fc - real diff 53 - 53 kh/s - 10598 tries
1: Nonce c052798595fda907bf02df16fd777552 - real diff 55 - 51 kh/s - 11574 tries
1: Nonce 98292fc31fc66948bdff33c20aabfce5 - real diff 53 - 52 kh/s - 13293 tries
1: Nonce 87cea0531b4399b7fb26ab699833b08f - real diff 54 - 50 kh/s - 13506 tries
1: Nonce 1ba8022d3f85492d2389437a20162368 - real diff 60 - 47 kh/s - 13595 tries
[...]

nonce 1000, 600 sec, diff 55
6 miners searching for solutions at difficulty55 and condition 7a0f3
3: Nonce ae372e7ebb221bc0a35d9dd50b9e8d7f - real diff 60 - 49 kh/s - 1315 tries
4: Nonce 91114d7827e896947c6914f315cf826c - real diff 60 - 39 kh/s - 1832 tries
3: Nonce c30a41aac62ff4408bb1e0e61cdce862 - real diff 60 - 29 kh/s - 3172 tries
6: Nonce ebc1419d737e66bdf577a3ae02338e22 - real diff 63 - 29 kh/s - 5975 tries
5: Nonce 3a5bc50d90c5830fad698349d25a2352 - real diff 57 - 25 kh/s - 7473 tries
6: Nonce 9d9de1b42ba0454dda0585a006a90d2a - real diff 60 - 40 kh/s - 11476 tries
1: Nonce 1ba8022d3f85492d2389437a20162368 - real diff 60 - 28 kh/s - 13595 tries
4: Nonce 8dc344bef72ae0c47dc2753b851011e0 - real diff 57 - 26 kh/s - 14247 tries
3: Nonce c4ecc01d5094448b7856499429269b55 - real diff 60 - 26 kh/s - 16946 tries
5: Nonce 4842e3a593b0b12fb5e7a203550d16b0 - real diff 60 - 48 kh/s - 17497 tries
4: Nonce 038abb11bbece5ea556648f2ad52d073 - real diff 57 - 27 kh/s - 18651 tries
6: Nonce 6714aef6f6473ba87f30149202c3e52d - real diff 60 - 25 kh/s - 19039 tries

"""
