
import sys

# custom modules
sys.path.append('../modules')
from hmac_drbg import DRBG


if __name__ == '__main__':
    gen = DRBG(b"secret seed")
    data = gen.generate(8)
    print(data)  # b'o\xf7\xc8\x0b\x11+\x9f\x93'

    gen = DRBG(b"Public Seed for a big file")
    # Size in Gb - No more than 4Gb from a single seed
    GB = 1
    # CHUNK_SIZE = 65536  # time 3m52.150s
    # CHUNK_SIZE = 1024  # time 3m31.672s
    CHUNK_SIZE = 1024*4  # time 3m20.990s

    COUNT = GB * 1024 * 1024 * 1024 // CHUNK_SIZE

    with open('rnd.bin', 'wb') as f:
        for chunks in range(COUNT):
            f.write(gen.generate(CHUNK_SIZE))

    """
    b'o\xf7\xc8\x0b\x11+\x9f\x93'
    
    sha256sum rnd.bin
    71b6de357fe8280ed6a21065465fb6d678bc0a26b7e9597ecc49cda6af14ec79  rnd.bin
    
    sha512sum rnd.bin
    2209cf1429a656fc67fba243f0cce9b6ac4b9a6be9c62eaa03a26b7cabd8de8359236b4686ad6f2f4b7f18b5db0b08cd5ca0fec1429309647dc73985a6fa5a4c  rnd.bin
    
    cksfv rnd.bin
    ./rnd.bin B6BB91CF
    """
