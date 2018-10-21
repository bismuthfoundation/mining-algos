# Just quick draft/ideas/general plan

Possibly to be split into several posts.

re-integrate content from https://github.com/bismuthfoundation/mining-algos/blob/master/Docs/Fork-FAQ.md
especially bis long term view on fpga/asic (important I think)

## Threat identification

- Bismuth network monitoring pages
- pools
- miners themselves reporting anomalies
- regular exchange dumps
- internal research on fpga capabilities, work with fpga devs.

## Threat emergency response

- block the main abuser
- require a higher end fpga hardware to mine. 
- was fpga with little ram => use significant ram

The constraints:
- Require the minimal amount of ram to penalize the attacker a lot, the rest of miners a little only
- Still is fast to verify on nodes and pools, even with minimal specs. A mining algo has to be both hard to compute and easy to check.
- Needs only minimal change to current GPU miners, so it can be implemented quickly by pools
- Introduce some memory bandwith limit so high end fpgas withh ddr4 still can mine, but do not have a 10x performance advantage.

## Bismuth Heavy3

See the docs with slides and pdf
https://github.com/bismuthfoundation/mining-algos/blob/master/Docs/

The idea behind the "Heavy3" algo designed by EggdraSyl is both simple and effective:  
require a read from a random offset in a fixed lookup table, for each tested nonce.

This concept can be applied to any other mining algorithm as an additional layer to protect against a similar attack.
Whatever the matching algorithm uses hashcasdh or not (bismuth does not) is irrelevant.

The final hash state that is tested is a vector of 32 bits words.
Since it's a hash result, it can be considered as a random vector, it can contain anything, and you can't reverse the process - this is a hash core property -
The lookup table also contains random data (*can give more details about the gen used and how we can tell it's random data*)
For each nonce, the extra step is applying a XOR transform to the hash output, given a random vector from the lookup table, with the index begin determined by the hash itself, therefore at a random, non predictable, location.
The result - xor'd hash state - is considered as the input vector to the difficulty matching function.

- This transformation does not affect the probability of finding a good candidate
- it does not change the hashing algorithm itself
- it does not change the difficulty matching algorithm either.
- It required reading of about 8 words from a random index for every tried nonce
- The miner has to keep a copy of the whole lookup table in memory at all time

This is then a generic tweak that can be applied instantly to any other crypto.


## Benefits of Bismuth Difficulty controller algorithm

- not too reactive: does not overcompensate when a pool or big miner drops off the net
- not too slow: has to react reasonably quickly to a long term hash rate increase
- adjustable: on fork, we programmatically dropped the diff by estimating whhat would the new hash be.
  We underestimated the hash, but the system worked well: diff dropped, and the algo then reached stability in a few days only.
  
  

