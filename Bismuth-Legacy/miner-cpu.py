"""
Demo cpu miner for Bismuth Legacy Algorithm

Derived from https://github.com/maccaspacca/Optipoolware/blob/master/optihash/optihash.py
"""

import random
import sys
import time
from hashlib import sha224
from multiprocessing import Process

# custom modules
sys.path.append('../modules')
import helpers
import vectors

NONCE_COUNT = 10000

# To get reproducible results
SEED = 'SOME_FIXED_BUFFER'

THREAD_COUNT = 1

# A very low diff target for CPU tests
DIFF = 50


def miner(q, address, db_block_hash, diff, mining_condition):
    tries = 0
    # One reproducible seed per thread
    random.seed(SEED + str(q))
    try_array = [('%0x' % random.getrandbits(32)) for i in range(NONCE_COUNT)]
    timeout = time.time() + 20
    t1 = time.time()

    # temp = dict()
    while t1 < timeout:
        try:
            tries = tries + 1
            # generate the "address" of a random backyard that we will sample in this try
            seed = ('%0x' % random.getrandbits(128 - 32))
            # this part won't change, so concat once only
            prefix = address + seed
            # This is where the actual hashing takes place
            possibles = [nonce for nonce in try_array if
                         mining_condition in (sha224((prefix + nonce + db_block_hash).encode("utf-8")).hexdigest())]
            # hashrate calculation
            try:
                t2 = time.time()
                khs = int((NONCE_COUNT / (t2 - t1)) / 1000)
            except Exception as e:
                khs = 1
            if possibles:
                for nonce in possibles:
                    # add the seed back to get a full  nonce
                    nonce = seed + nonce
                    real_diff = helpers.diffme_legacy(address[:56], nonce, db_block_hash)
                    if real_diff < diff:
                        pass
                    else:
                        print("{}: Nonce {} - real diff {} - {} kh/s".format(q, nonce, real_diff, khs))
                        # temp[nonce] = real_diff
            t1 = time.time()
        except Exception as e:
            print(e)
    # print(temp)


if __name__ == '__main__':
    instances = range(THREAD_COUNT)
    # For reproducible tests
    random.seed(SEED)
    mining_condition_bin = helpers.bin_convert_orig(vectors.BLOCK_HASH)[:DIFF]
    diff_hex = int((DIFF / 8) - 1)
    mining_condition = vectors.BLOCK_HASH[:diff_hex]

    for q in instances:
        p = Process(target=miner, args=(
        str(q + 1), vectors.ADDRESS, vectors.BLOCK_HASH, DIFF, mining_condition))
        p.daemon = True
        p.start()
    print("{} miners searching for solutions at difficulty {} and condition {}"
          .format(THREAD_COUNT, DIFF, mining_condition))

    for q in instances:
        p.join()
    p.terminate()
