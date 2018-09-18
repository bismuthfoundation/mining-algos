"""
Bismuth Legacy Algorithm

Check test vectors with pure python lib
"""

import sys

# custom modules
sys.path.append('../modules')
import helpers
import vectors
import pp_sha224


if __name__ == '__main__':
    print("Checking nonce for Legacy Algorithm, block_hash={}".format(vectors.BLOCK_HASH))
    for nonce, diff in vectors.NONCES['legacy'].items():
        real_diff = helpers.diffme_legacy(vectors.ADDRESS, nonce, vectors.BLOCK_HASH)
        # already done in diffme, but recalc to print
        hash = pp_sha224.sha224((vectors.ADDRESS + nonce + vectors.BLOCK_HASH).encode("utf-8")).hexdigest()
        print("Nonce {}: diff {} vs planned {}".format(nonce, diff, real_diff))
        print(" Hash is {}".format(hash))
