"""

"""
import mmap
import struct
import sys

# custom modules
sys.path.append('../modules')


def read_int_from_map(map, index):
    return struct.unpack('I', map[4 * index:4 * index + 4])[0]


def mmap_read():
    # https://stackoverflow.com/questions/24381090/performance-issue-with-reading-integers-from-a-binary-file-at-specific-locations
    with open("rnd.bin", "rb+") as f:
        # memory-map the file, size 0 means whole file
        with mmap.mmap(f.fileno(), 0) as map:
            # https: // docs.python.org / 3 / library / mmap.html
            # read content via slice notation
            print(read_int_from_map(map, 0))  # 3001179434
            print(read_int_from_map(map, 10))  # 3440476437
            print(read_int_from_map(map, 1024))  # 2707377409
        # Don't forget map.close() if you don't use context managers.


if __name__ == '__main__':
    mmap_read()

"""
3001179434
3440476437
2707377409
"""
