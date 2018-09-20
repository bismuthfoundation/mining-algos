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
SEED = 'Bismuth_Heavy_3'

THREAD_COUNT = 6

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
    temp = dict()
    while t1 < timeout:
        try:
            tries = tries + 1
            nonce_array = ["{:032x}".format(random.getrandbits(128)) for i in range(NONCE_COUNT)]
            possibles = [nonce for nonce in nonce_array if
                         mining_condition in (
                             annealing.anneal3(MMAP, int.from_bytes(
                                 sha224((address + nonce + db_block_hash).encode("utf-8")).digest(), 'big')))]
            # hash rate calculation
            try:
                t2 = time.time()
                khs = int((NONCE_COUNT / (t2 - t1)) / 1000)
            except Exception as e:
                khs = 1
            if possibles:
                for nonce in possibles:
                    real_diff = helpers.diffme_heavy3(MMAP, address, nonce, db_block_hash)
                    if real_diff <= diff:
                        pass
                        # print("Real diff {}".format(real_diff))
                    else:
                        print("{}: Nonce {} - real diff {} - {} kh/s - {} tries".format(q, nonce, real_diff, khs, tries))
                        temp[nonce] = real_diff
            t1 = time.time()
        except Exception as e:
            print(e)
    print(temp)


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
6 miners searching for solutions at difficulty 50 and condition 7a0f3
5: Nonce c27de5762deb69cdb3f50b6968bb570d - real diff 54 - 47 kh/s - 1 tries
5: Nonce db0d95f47a070b01c81d87bb8f614747 - real diff 54 - 49 kh/s - 71 tries
5: Nonce 3e2b67d6eb561831f22f1f9f85f0319d - real diff 53 - 57 kh/s - 121 tries
4: Nonce 7c5beead8ec238f69d1936ab0621a0ef - real diff 54 - 31 kh/s - 166 tries
6: Nonce 7a63750ab36319f6f70d31ab4fe5a8c1 - real diff 54 - 51 kh/s - 197 tries
6: Nonce d492720ec4144f6f88ff8f43d00c17c4 - real diff 54 - 40 kh/s - 205 tries
6: Nonce 9922892d8f88353ef896a26a233b39a0 - real diff 54 - 31 kh/s - 281 tries
3: Nonce eb2305473d50f728d87c8496733a4f16 - real diff 57 - 29 kh/s - 379 tries
1: Nonce 74aca678a02cf809a4b5286c0a3132d1 - real diff 52 - 58 kh/s - 473 tries
5: Nonce 69da5c246606f6cc2935871346fc6360 - real diff 52 - 31 kh/s - 602 tries
2: Nonce 873b3f0130061e62f84e56405a603a6f - real diff 53 - 59 kh/s - 605 tries
3: Nonce 79a1c047cf62837daeaa3204454f2582 - real diff 53 - 31 kh/s - 598 tries
1: Nonce cef93c8ea234c90758d421a38f41cc98 - real diff 53 - 27 kh/s - 644 tries
5: Nonce 386fe932d852be0006140794ca9c3b55 - real diff 52 - 26 kh/s - 717 tries
"""
