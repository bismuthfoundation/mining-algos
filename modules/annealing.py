
import mmap
import os
import struct
import sys

__version__ = '0.0.3'


RND_LEN = 0

MMAP = None
F = None


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


def anneal_hash(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    res = ''
    for i in range(7):
        part = n & 0xffffffff
        n = n >> 32
        index = part % RND_LEN
        value = part ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        # difference with anneal224: keep word order.
        res = "{:08x}".format(value) + res
    return res


def anneal_hash_test(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    res = ''
    Fvalue = struct.unpack('I', mmap[1024:1028])[0]
    for i in range(7):
        part = n & 0xffffffff
        n = n >> 32
        value = part ^ Fvalue
        # difference with anneal224: keep word order.
        res = "{:08x}".format(value) + res
    return res


def anneal_hash_verbose(mmap, n):
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
        # difference with anneal224: keep word order.
        res = "{:08x}".format(value) + res
    return res


def anneal3(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    h7 = n & 0xffffffff
    n = n >> 32
    index = ((h7 & ~0x7) % RND_LEN) * 4
    f1 = struct.unpack('I', mmap[index:index + 4])[0]
    value = h7 ^ struct.unpack('I', mmap[index:index + 4])[0]
    res = "{:08x}".format(value)
    for i in range(6):
        index += 4
        h = n & 0xffffffff
        n = n >> 32
        value = h ^ struct.unpack('I', mmap[index:index + 4])[0]
        res = "{:08x}".format(value) + res
    return res


def anneal3_verbose(mmap, n):
    """
    Converts 224 bits number into annealed version, hexstring

    :param n: a 224 = 7x32 bits
    :return:  56 char in hex encoding.
    """
    print("n {:032x}".format(n))

    h7 = n & 0xffffffff
    n = n >> 32
    index = ((h7 & ~0x7) % RND_LEN)
    print("h7 {:08x}".format(h7))
    print("index {:08x}".format(index))
    f1 = struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
    print("F7 {:08x}".format(f1))
    value = h7 ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
    print("v7 {:08x}".format(value))
    res = "{:08x}".format(value)
    for i in range(6):
        index += 1
        h = n & 0xffffffff
        n = n >> 32
        print("h {:08x}".format(h))
        print("index {:08x}".format(index))
        value = h ^ struct.unpack('I', mmap[4 * index:4 * index + 4])[0]
        print("v {:08x}".format(value))
        res = "{:08x}".format(value) + res
    return res


def junction_open():
    """
    Opens the Junction MMapped file
    """
    global F
    global MMAP
    global RND_LEN
    map = './rnd.bin' if os.path.isfile('./rnd.bin') else '../CSPRNG/rnd.bin'
    F = open(map, "rb+")
    # memory-map the file, size 0 means whole file
    MMAP = mmap.mmap(F.fileno(), 0)
    RND_LEN = os.path.getsize(map) // 4


def junction_close():
    """
    Close the MMAP access, HAS to be called at end of program.
    """
    global F
    global MMAP
    if MMAP:
        MMAP.close()
    if F:
        F.close()
