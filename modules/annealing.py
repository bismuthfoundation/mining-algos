
import struct


RND_LEN = 0


def read_int_from_map(map, index):
    return struct.unpack('I', map[4 * index:4 * index + 4])[0]


def anneal128(mmap, n):
    """
    Converts 128 bits number into annealed version, hexstring

    :param n: a 128 = 4x32 bits, 16 bytes,
    :return: 32 char in hex encoding.
    """
    res = ''
    # print("n {:032x}".format(n))
    for i in range(4):
        part = n & 0xffffffff
        n = n >> 32
        # print("n {:08x}".format(part))
        index = part % RND_LEN
        # print("i {:08x}".format(index))
        value = part ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        # print("v {:08x}".format(value))
        res += "{:08x}".format(value)
    return res
    # Variant : convert 32 ascii chars into a 32 bytes wide byte array. More entropy in nonce.
    # but means less possible offsets from the file.


def anneal224(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    res = ''
    # print("n {:032x}".format(n))
    for i in range(7):
        part = n & 0xffffffff
        n = n >> 32
        # print("n {:08x}".format(part))
        index = part % RND_LEN
        # print("i {:08x}".format(index))
        value = part ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        # print("v {:08x}".format(value))
        res += "{:08x}".format(value)
    return res


def anneal128_verbose(mmap, n):
    """
    Converts 128 bits number into annealed version, hexstring

    :param n: a 128 = 4x32 bits, 16 bytes,
    :return: 32 char in hex encoding.
    """
    res = ''
    print("n {:032x}".format(n))
    for i in range(4):
        part = n & 0xffffffff
        n = n >> 32
        print("n {:08x}".format(part))
        index = part % RND_LEN
        print("i {:08x}".format(index))
        value = part ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        print("v {:08x}".format(value))
        res += "{:08x}".format(value)
    return res
    # Variant : convert 32 ascii chars into a 32 bytes wide byte array. More entropy in nonce.
    # but means less possible offsets from the file.


def anneal224_verbose(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    res = ''
    # print("n {:032x}".format(n))
    for i in range(7):
        part = n & 0xffffffff
        n = n >> 32
        print("n {:08x}".format(part))
        index = part % RND_LEN
        print("i {:08x}".format(index))
        value = part ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        print("v {:08x}".format(value))
        res += "{:08x}".format(value)
    return res
