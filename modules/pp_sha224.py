"""
Pure Python SHA224 implementation for test vectors details

TODO: find reference
"""



class Hash(object):
    """ Common class for all hash methods.
    It copies the one of the hashlib module (https://docs.python.org/3.5/library/hashlib.html).
    """

    def __init__(self, *args, **kwargs):
        """
        Create the Hash object.
        """
        self.name = self.__class__.__name__  # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.name
        self.byteorder = 'little'
        self.digest_size = 0  # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.digest_size
        self.block_size = 0  # https://docs.python.org/3.5/library/hashlib.html#hashlib.hash.block_size

    def __str__(self):
        return self.name

    def update(self, arg):
        """
        Update the hash object with the object arg, which must be interpretable as a buffer of bytes.
        """
        pass

    def digest(self):
        """
        Return the digest of the data passed to the update() method so far.
        This is a bytes object of size digest_size which may contain bytes in the whole range from 0 to 255.
        """
        return b""

    def hexdigest(self):
        """
        Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits.
        This may be used to exchange the value safely in email or other non-binary environments.
        """
        digest = self.digest()
        raw = digest.to_bytes(self.digest_size, byteorder=self.byteorder)
        format_str = '{:0' + str(2 * self.digest_size) + 'x}'
        return format_str.format(int.from_bytes(raw, byteorder='big'))


def tohex(digest):
    raw = digest  # .to_bytes(self.digest_size, byteorder=self.byteorder)
    format_str = '{:08x}'
    return format_str.format(int.from_bytes(raw, byteorder='big'))


def leftrotate(x, c):
    """ Left rotate the number x by c bytes."""
    x &= 0xFFFFFFFF
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def rightrotate(x, c):
    """ Right rotate the number x by c bytes."""
    x &= 0xFFFFFFFF
    return ((x >> c) | (x << (32 - c))) & 0xFFFFFFFF


def leftshift(x, c):
    """ Left shift the number x by c bytes."""
    return x << c


def rightshift(x, c):
    """ Right shift the number x by c bytes."""
    return x >> c


class sha224(Hash):
    """SHA224 hashing, see https://en.wikipedia.org/wiki/SHA-2#Pseudocode."""

    def __init__(self, arg=None):
        self.name = "SHA224"
        self.byteorder = 'big'
        self.block_size = 64
        self.digest_size = 32
        # Note 2: For each round, there is one round constant k[i] and one entry in the message schedule array w[i], 0 ≤ i ≤ 63
        # Note 3: The compression function uses 8 working variables, a through h
        # Note 4: Big-endian convention is used when expressing the constants in this pseudocode,
        #         and when parsing message block data from bytes to words, for example,
        #         the first word of the input message "abc" after padding is 0x61626380

        # Initialize hash values:
        # (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):

        h0 = 0xc1059ed8
        h1 = 0x367cd507
        h2 = 0x3070dd17
        h3 = 0xf70e5939
        h4 = 0xffc00b31
        h5 = 0x68581511
        h6 = 0x64f98fa7
        h7 = 0xbefa4fa4

        # Initialize array of round constants:
        # (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311):
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        # Store them
        self.hash_pieces = [h0, h1, h2, h3, h4, h5, h6, h7]
        if arg:
            self.update(arg)

    def update(self, arg):
        h0, h1, h2, h3, h4, h5, h6, h7 = self.hash_pieces
        # 1. Pre-processing, exactly like MD5
        data = bytearray(arg)
        orig_len_in_bits = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
        # 1.a. Add a single '1' bit at the end of the input bits
        data.append(0x80)
        # 1.b. Padding with zeros as long as the input bits length ≡ 448 (mod 512)
        while len(data) % 64 != 56:
            data.append(0)
        # 1.c. append original length in bits mod (2 pow 64) to message
        data += orig_len_in_bits.to_bytes(8, byteorder='big')
        assert len(data) % 64 == 0, "Error in padding"

        # print(tohex(data), len(data))

        # 2. Computations
        # Process the message in successive 512-bit = 64-bytes chunks:
        for offset in range(0, len(data), 64):
            # 2.a. 512-bits = 64-bytes chunks
            chunks = data[offset: offset + 64]
            w = [0 for i in range(64)]
            # 2.b. Break chunk into sixteen 32-bit = 4-bytes words w[i], 0 ≤ i ≤ 15
            for i in range(16):
                w[i] = int.from_bytes(chunks[4 * i: 4 * i + 4], byteorder='big')
            # 2.c.  Extend the first 16 words into the remaining 48
            #       words w[16..63] of the message schedule array:
            for i in range(16, 64):
                s0 = (rightrotate(w[i - 15], 7) ^ rightrotate(w[i - 15], 18) ^ rightshift(w[i - 15], 3)) & 0xFFFFFFFF
                s1 = (rightrotate(w[i - 2], 17) ^ rightrotate(w[i - 2], 19) ^ rightshift(w[i - 2], 10)) & 0xFFFFFFFF
                w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF
            # for wi in w:
            #	print("%08x " % wi)
            # 2.d. Initialize hash value for this chunk
            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
            # 2.e. Main loop, cf. https://tools.ietf.org/html/rfc6234
            for i in range(64):
                S1 = (rightrotate(e, 6) ^ rightrotate(e, 11) ^ rightrotate(e, 25)) & 0xFFFFFFFF
                ch = ((e & f) ^ ((~e) & g)) & 0xFFFFFFFF
                temp1 = (h + S1 + ch + self.k[i] + w[i]) & 0xFFFFFFFF
                S0 = (rightrotate(a, 2) ^ rightrotate(a, 13) ^ rightrotate(a, 22)) & 0xFFFFFFFF
                maj = ((a & b) ^ (a & c) ^ (b & c)) & 0xFFFFFFFF
                temp2 = (S0 + maj) & 0xFFFFFFFF

                new_a = (temp1 + temp2) & 0xFFFFFFFF
                new_e = (d + temp1) & 0xFFFFFFFF
                # Rotate the 8 variables
                a, b, c, d, e, f, g, h = new_a, a, b, c, new_e, e, f, g

            # Add this chunk's hash to result so far:
            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF
            # print("%08x %08x %08x %08x %08x %08x %08x %08x" % (h0, h1, h2, h3, h4, h5, h6, h7))
        # 3. Conclusion
        self.hash_pieces = [h0, h1, h2, h3, h4, h5, h6, h7]

    def digest(self):
        # h0 append h1 append h2 append h3 append h4 append h5 append h6 append h7
        return sum(leftshift(x, 32 * i) for i, x in enumerate(self.hash_pieces[::-1]))


def hash_SHA224(data):
    """ Shortcut function to directly receive the hex digest from SHA2(data)."""
    h = sha224()
    if isinstance(data, str):
        data = bytes(data, encoding='utf8')
    h.update(data)
    return h.hexdigest()
