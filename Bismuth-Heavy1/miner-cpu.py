"""
Demo cpu miner for Bismuth HHeavy 1 Algorithm

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


NONCE_COUNT = 1000

# To get reproducible results
SEED = 'SOME_FIXED_BUFFER1'

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
            possibles = []
            nonce_array = [random.getrandbits(128) for i in range(NONCE_COUNT)]
            try_array = [annealing.anneal128(MMAP, n) for n in nonce_array]
            # try_array = ["{:032x}".format(n) for n in nonce_array]
            for i in range(NONCE_COUNT):
                hash = sha224((address + try_array[i] + db_block_hash).encode("utf-8")).digest()
                hash = int.from_bytes(hash, 'big')
                annealed_sha = annealing.anneal224(MMAP, hash)
                if mining_condition in annealed_sha:
                    possibles.append((nonce_array[i], try_array[i], annealed_sha))
            # hashrate calculation
            try:
                t2 = time.time()
                khs = int((NONCE_COUNT / (t2 - t1)) / 1000)
            except Exception as e:
                khs = 1
            if possibles:
                for nonce in possibles:
                    real_diff = helpers.diffme_heavy1(address[:56], nonce[1], nonce[2], db_block_hash)
                    if real_diff <= diff:
                        pass
                    else:
                        print("{}: Nonce {} - real diff {} - {} kh/s - {} tries".format(q, "{:032x}".format(nonce[0]), real_diff, khs, tries))
                        # temp["{:032x}".format(nonce[0])] = real_diff

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
No mix
SEED = 'SOME_FIXED_BUFFER1'
NONCE_COUNT = 10000
1 Thread
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce 273df90281c76d7477b2649a7085f28a - real diff 55 - 293 kh/s - 56 tries
1: Nonce ce503eef86bcada64936a58472fb7d64 - real diff 53 - 292 kh/s - 64 tries
1: Nonce 4c4d83518f75a0ae14fffd4b4e27530c - real diff 53 - 393 kh/s - 127 tries
1: Nonce ee59a2037547618e633619e6b8ef8688 - real diff 53 - 407 kh/s - 176 tries
1: Nonce 18329e48d5358397ef69af60ed73559d - real diff 53 - 402 kh/s - 177 tries
1: Nonce 1758042dc7077e7aa4e92285c9ecc6d3 - real diff 53 - 387 kh/s - 223 tries
1: Nonce 20cc3a431c52ea7eb36a734d413e1fc4 - real diff 53 - 396 kh/s - 224 tries
1: Nonce b1e0812729759ba9550ed845a81d1240 - real diff 53 - 409 kh/s - 256 tries
1: Nonce 168fa12e518b2eec5bb04a84ca6fd04d - real diff 60 - 404 kh/s - 304 tries
1: Nonce 9715879ffb3301422c98da83f5a40908 - real diff 52 - 379 kh/s - 334 tries
1: Nonce 872fa294be59929e8d57bfd894faf112 - real diff 55 - 412 kh/s - 364 tries
1: Nonce 5d617a47df64d68a1fb943e7599d3e49 - real diff 53 - 400 kh/s - 365 tries

Without prefix opti, for clarity
SEED = 'SOME_FIXED_BUFFER1'
NONCE_COUNT = 10000
1 Thread
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce 33f9f1c199c432389cd016c891b647e8 - real diff 53 - 339 kh/s - 49 tries
1: Nonce 3de382960576c364f3284034bb68da93 - real diff 53 - 324 kh/s - 259 tries
1: Nonce d05a7e4f9848a753862bda9e2d89b366 - real diff 52 - 330 kh/s - 271 tries

With only nonce fuzzing:
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce 80f2fdbc8c3074674aa2fb0afa8fb613 - real diff 53 - 90 kh/s - 1013 tries
1: Nonce 7b8a5fedf2f5cc5e88d6cf260d8bbbef - real diff 53 - 87 kh/s - 2058 tries
1: Nonce 7a06fe949c81feb46f3fcdecf1f8f6f6 - real diff 53 - 86 kh/s - 2462 tries

With nonce and final hash fuzzing, nonce 1000, 60 sec, diff 50
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce 4a94ef265a682330e9d0d331aca248bc - real diff 52 - 38 kh/s - 308 tries
1: Nonce a523712d06cc0b68fc0efd9b13166aed - real diff 52 - 38 kh/s - 332 tries
1: Nonce 774e3ecaf0795d5499b36e630dc98b37 - real diff 53 - 38 kh/s - 1207 tries
1: Nonce 944983737dfcbbca6103db5894ad1711 - real diff 52 - 36 kh/s - 1490 tries
1: Nonce c0dd362f98f2806389907373d6577246 - real diff 54 - 38 kh/s - 1750 tries
1: Nonce d6c7fbdb89ac764539d876033ab9e0dc - real diff 53 - 39 kh/s - 1836 tries
1: Nonce f25d50198e0d1bb1c3e89df775cc15da - real diff 53 - 37 kh/s - 1878 tries
1: Nonce 398663b2e10fa34a34dc6353384eb193 - real diff 53 - 37 kh/s - 1956 tries


With only final hash fuzzing, nonce 1000, 60 sec, diff 50
1 miners searching for solutions at difficulty 50 and condition 7a0f3
1: Nonce cc4b087d72346eac77797378d55fe6b3 - real diff 53 - 54 kh/s - 1334 tries
1: Nonce 7760e3b68a55273f2dbc5e93169c4d66 - real diff 55 - 53 kh/s - 2132 tries

With nonce and final hash fuzzing, nonce 1000, 600 sec, diff 55
4 miners searching for solutions at difficulty 55 and condition 7a0f3
3: Nonce de9f51522185677d6f10fae2af64113b - real diff 57 - 37 kh/s - 4653 tries
2: Nonce ea9f41ae3a123982e6245ee71cf7fdfd - real diff 60 - 31 kh/s - 6509 tries
3: Nonce 04365bf049c897b344a9e1b2b6faa6df - real diff 60 - 37 kh/s - 7752 tries
3: Nonce d63d6478c4113ccb842619a6ca52e1d9 - real diff 57 - 29 kh/s - 11205 tries
2: Nonce 1f22e8a67dade1c405f0ab440fc1d973 - real diff 60 - 36 kh/s - 12646 tries
1: Nonce 20b16af74ce134246098f047c61de099 - real diff 57 - 35 kh/s - 14590 tries
2: Nonce 38941507759f5dc76aa6fb0df84b4d67 - real diff 63 - 30 kh/s - 17841 tries


"""
