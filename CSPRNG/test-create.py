
import sys

# custom modules
sys.path.append('../modules')
from hmac_drbg import DRBG


if __name__ == '__main__':
    gen = DRBG(b"secret seed")
    data = gen.generate(8)
    print(data)  # b'o\xf7\xc8\x0b\x11+\x9f\x93'

    gen = DRBG(b"secret seed 2 for a big file")
    # Size in Gb - No more than 4Gb from a single seed
    GB = 1
    # CHUNK_SIZE = 65536  # time 3m52.150s
    CHUNK_SIZE = 1024  # time 3m31.672s

    COUNT = GB * 1024 * 1024 * 1024 // CHUNK_SIZE

    with open('rnd.bin', 'wb') as f:
        for chunks in range(COUNT):
            f.write(gen.generate(CHUNK_SIZE))

    """
    b'o\xf7\xc8\x0b\x11+\x9f\x93'
    
    sha256sum rnd.bin
    1c09d31c708be829e7daffee7d16942fe9b5756ab8d27dab45c7020b413a78b5  rnd.bin
    
    sha512sum rnd.bin
    1995eba88542e028d43235232d134651224fb852e9d37a93af59b223cba2027f95fe5130c570d6b23beaae99108cc5710d7d652083efeb84b0bac844edee5177  rnd.bin
    
    cksfv rnd.bin
    ./rnd.bin F2F2B51D
    """
