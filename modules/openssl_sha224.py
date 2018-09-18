"""
A resumable implementation of SHA-256 using ctypes with the OpenSSL crypto library
Written by PM 2Ring 2014.11.13
From https://stackoverflow.com/questions/2130892/persisting-hashlib-state
"""

import os
from ctypes import *

SHA_LBLOCK = 16
SHA256_DIGEST_LENGTH = 32

class SHA256_CTX(Structure):
    _fields_ = [
        ("h", c_uint * 8),  # was c_long?
        ("Nl", c_long),
        ("Nh", c_long),
        ("data", c_long * SHA_LBLOCK),
        ("num", c_uint),
        ("md_len", c_uint)
    ]

HashBuffType = c_ubyte * SHA256_DIGEST_LENGTH

#crypto = cdll.LoadLibrary("libcrypto.so")
crypto = cdll.LoadLibrary("libeay32.dll" if os.name == "nt" else "libssl.so")

class sha256(object):
    digest_size = SHA256_DIGEST_LENGTH

    def __init__(self, datastr=None):
        self.ctx = SHA256_CTX()
        crypto.SHA256_Init(byref(self.ctx))
        print("I", ["{:08X}".format(a) for a in self.ctx.h])
        if datastr:
            self.update(datastr)

    def update(self, datastr):
        crypto.SHA256_Update(byref(self.ctx), datastr, c_int(len(datastr)))
        # ctx.h is not updated yet.
        print("U", ["{:08X}".format(a) for a in self.ctx.h])

    def _copy_ctx(self):
        # Clone the current context
        ctx = SHA256_CTX()
        pointer(ctx)[0] = self.ctx
        return ctx

    def copy(self):
        other = sha256()
        other.ctx = self._copy_ctx()
        return other

    def digest(self):
        # Preserve context in case we get called before hashing is
        # really finished, since SHA256_Final() clears the SHA256_CTX
        ctx = self._copy_ctx()
        hashbuff = HashBuffType()
        crypto.SHA256_Final(hashbuff, byref(self.ctx))
        # Only here ctx.h is updated in one go.
        print("D", ["{:08X}".format(a) for a in self.ctx.h])
        self.ctx = ctx
        return bytearray(hashbuff)

    def hexdigest(self):
        digest = self.digest()
        format_str = '{:0' + str(2 * 32) + 'x}'
        return format_str.format(int.from_bytes(digest, byteorder='big'))
        """
        return digest
        raw = digest.to_bytes(32, byteorder='big')
        format_str = '{:0' + str(2 * 32) + 'x}'
        return format_str.format(int.from_bytes(raw, byteorder='big'))
        """


#Tests
def main():
    # import cPickle
    import hashlib

    data = ("Nobody expects ", "the spammish ", "imposition!")

    print("rehash\n")

    shaA = sha256(''.join(data).encode('utf-8'))
    print(shaA.hexdigest())
    # print(repr(shaA.digest()))
    # print("digest size =", shaA.digest_size)

    shaB = sha256()
    shaB.update(data[0].encode('utf-8'))
    print(shaB.hexdigest())

    #Test pickling
    """
    sha_pickle = cPickle.dumps(shaB, -1)
    print "Pickle length:", len(sha_pickle)
    shaC = cPickle.loads(sha_pickle)
    
    shaC.update(data[1])
    print shaC.hexdigest()

    #Test copying. Note that copy can be pickled
    shaD = shaC.copy()

    shaC.update(data[2])
    print shaC.hexdigest()
    """

    #Verify against hashlib.sha256()
    print("\nhashlib\n")


    shaD = hashlib.sha256(''.join(data).encode('utf-8'))
    print(shaD.hexdigest())
    # print(repr(shaD.digest()))
    #print("digest size =", shaD.digest_size)

    shaE = hashlib.sha256(data[0].encode('utf-8'))
    print(shaE.hexdigest())

    """
    shaE.update(data[1])
    print shaE.hexdigest()

    #Test copying. Note that hashlib copy can NOT be pickled
    shaF = shaE.copy()
    shaF.update(data[2])
    print shaF.hexdigest()
    """


if __name__ == '__main__':
    main()
