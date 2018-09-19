"""
Test vectors for Bismuth PoW mining
"""


__version__ = '0.0.2'


# Test address (Genesis)
ADDRESS = '4edadac9093d9326ee4b17f869b14f1a2534f96f9c5d7b48dc9acaed'

# Test Block hash (Genesis)
BLOCK_HASH = '7a0f384876aca3871adbde8622a87f8b971ede0ed8ee10425e3958a1'

# Test nonces and matching diff
NONCES = {
    "legacy": {'5ead736b0456eee16a99edbbe5f8f2a0': 53,
               'a741a704541d0481c36356d1f7a5aa1d': 53,
               '350cb96f413cb1a16fd365f99747fefa': 53,
               '32d8df50d77198a9c093d7452167fe73': 53,
               '1dc2ec48a94f336b528d9b96c807fa72': 52,
               '13502107c07ef8f739d03bfb878191a6': 54,
               'fff30bd2e231ea901ec0046b8e84768d': 53,
               'fff30bd2e231ea901ec0046b7ff057d0': 53,
               'dfdca4760df296949c1c9cac326d824d': 55,
               '413403760dc9ab956ada1157b6f39f64': 60,
               'e95da0d77a84e5dd43a5d0e1e3a23ad5': 53,
               'c99235911b9858b9e887110f4b640a66': 53,
               'fba25c1dddb2ca9b9c709639d820438e': 53,
               '8550fe9fde36584bcb3e7168aa2f7eb6': 53},

    "heavy1-old": {'4a94ef265a682330e9d0d331aca248bc': 52,
               '20b16af74ce134246098f047c61de099': 57,
               'de9f51522185677d6f10fae2af64113b': 57,
               '04365bf049c897b344a9e1b2b6faa6df': 60,
               'd63d6478c4113ccb842619a6ca52e1d9': 57,
               'ea9f41ae3a123982e6245ee71cf7fdfd': 60,
               '1f22e8a67dade1c405f0ab440fc1d973': 60,
               '38941507759f5dc76aa6fb0df84b4d67': 63},

    "heavy1": {},

    "heavy2": {'fe29e15dcc7c65e05a3bd3cafc20ea9d': 52,
               'abcfd68fa8ce06a6889b6a6514efb45e': 53,
               'c60c26ea06aa3419fdee722e9a37dd3b': 54,
               'c35eb5707cd5465edf07beda747b2394': 54,
               '3a4df9b4ae1e3ec6cb6f377ce57ba72b': 53,
               '4c1cfba931716d80e32404d985cd4717': 52,
               'dcf3452b89d48cbd32bc1eb05044a3a2': 52,
               '2eadfddb3e959c9709342b77a29e2d82': 54,
               '0c03c050b8bc270f7af0d779ce26d1b1': 53,
               '856de8919191918952949b5f0eeaaf18': 53,
               '735de24cf32f7d91258c9bf958f96aa1': 53,
               'e7bbe22a02a7d88302bd81b9440ffd11': 54,
               'e13e1ad0ac35c3609bd3aaf39891e1fc': 53,
               'c052798595fda907bf02df16fd777552': 55,
               '98292fc31fc66948bdff33c20aabfce5': 53,
               '87cea0531b4399b7fb26ab699833b08f': 54,
               '1ba8022d3f85492d2389437a20162368': 60,
               'ae372e7ebb221bc0a35d9dd50b9e8d7f': 60,
               '4842e3a593b0b12fb5e7a203550d16b0': 60}
    }


