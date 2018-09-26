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
            print(read_int_from_map(map, 0))  # 3786993664
            print(read_int_from_map(map, 10))  # 2908245643
            print(read_int_from_map(map, 1024))  # 1742706086
            #
            print("{:08x}".format(read_int_from_map(map, 0)))  # e1b8f000
            print("{:08x}".format(read_int_from_map(map, 10)))  # ad584e8b
            print("{:08x}".format(read_int_from_map(map, 1024)))  # 67df95a6
        # Don't forget map.close() if you don't use context managers.


if __name__ == '__main__':
    mmap_read()

"""
3786993664
2908245643
1742706086
e1b8f000
ad584e8b
67df95a6

"""
