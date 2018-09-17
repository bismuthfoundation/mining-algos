"""
Common helpers
"""


from hashlib import sha224


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

