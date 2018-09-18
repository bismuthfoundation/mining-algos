"""
Common helpers
"""


import annealing
from hashlib import sha224
import pp_sha224



bin_format_dict = dict((x, format(ord(x), '8b').replace(' ', '0')) for x in '0123456789abcdef')


def bin_convert(string):
    return ''.join(bin_format_dict[x] for x in string)


def bin_convert_orig(string):
    return ''.join(format(ord(x), '8b').replace(' ', '0') for x in string)


def diffme_legacy(pool_address, nonce, db_block_hash):
    # minimum possible diff
    diff = 1
    diff_result = 0
    mining_hash = bin_convert(sha224((pool_address + nonce + db_block_hash).encode("utf-8")).hexdigest())
    mining_condition = bin_convert(db_block_hash)
    while mining_condition[:diff] in mining_hash:
        diff_result = diff
        diff += 1
    return diff_result


def diffme_heavy1(pool_address, nonce, fuzzed, db_block_hash):
    # minimum possible diff
    diff = 1
    diff_result = 0
    mining_hash = bin_convert(fuzzed)
    mining_condition = bin_convert(db_block_hash)
    while mining_condition[:diff] in mining_hash:
        diff_result = diff
        diff += 1
    return diff_result


def diffme_heavy1_full(map, pool_address, nonce, db_block_hash):
    """
    TODO: Make a clean class
    """
    diff = 1
    diff_result = 0
    # Calc fuzzed
    nonce =  int(nonce, 16)
    # print("nonce {:032x}".format(nonce))
    annealed_nonce = annealing.anneal128(map, nonce)
    # print("a_nonce {}".format(annealed_nonce))
    hash = sha224((pool_address + annealed_nonce + db_block_hash).encode("utf-8")).digest()
    hash = int.from_bytes(hash, 'big')
    annealed_sha = annealing.anneal224(map, hash)
    # print("a_sha {}".format(annealed_sha))
    bin_annealed_sha = bin_convert(annealed_sha)
    mining_condition = bin_convert(db_block_hash)
    while mining_condition[:diff] in bin_annealed_sha:
        diff_result = diff
        diff += 1
    return diff_result


def diffme_legacy_pp(pool_address, nonce, db_block_hash):
    # minimum possible diff
    diff = 1
    diff_result = 0
    mining_hash = bin_convert(pp_sha224.sha224((pool_address + nonce + db_block_hash).encode("utf-8")).hexdigest())
    mining_condition = bin_convert(db_block_hash)
    while mining_condition[:diff] in mining_hash:
        diff_result = diff
        diff += 1
    return diff_result
