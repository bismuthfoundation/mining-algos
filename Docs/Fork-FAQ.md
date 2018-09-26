# Bismuth PoW algorithm fork explained

## Why?

Lately, a solo miner with huge hash power was mining on Bismuth.  
It's been confirmed that it's an FPGA mining operation, that has a way better Hash/Watt than GPUs.  
The resulting hash - 60+% of the network, solo + pool - showed no mercy to the coin profitability, and is careless of the network: that solo miner does not even embed transactions in its blocks.  

This scenario is common among PoW coins: 
- A big op comes and mines with a lot of hash.   
- Difficulty skyrockets.  
- Previous miners go nuts.  
- Big miner Dumps.  
- Price drops.  

We had to react. One miner having so much power is not an option. It's a threat to the coin from several angles.

This is sad because fundamentally, we have nothing against FPGA miners.  
Hell, I do work on fpgas myself and speak with fpgas devs.  
Some did their maths and estimated how much % of the total net the publicly available fpgas could take over (like 10%)
We have no issue with that.  
We have no issue either with a dedicated fpga miner that would mine Bis, be open and/or easily available.

But we can't accept a single op getting that much % of BIS.  
Decentralization is a core belief of crypto.

## Emergency response

What makes the fpga mining so efficient is that the legacy Bismuth Mining algo requires only processing power, but no memory.  
After careful research and tests, I came up with a slight change to the current mining algo that:
- Is memory hard
- Would block or penalize this specific miner a lot
- Still is fast to verify on nodes
- Needs only minimal change to current GPU miners, so it can be implemented quickly by pools  

The "Bismuth Heavy 3" mining algorithm was born, and will be used after the fork.

## Mid and Long term

We still are in favor of fpga and - why not - dedicated asics hardware for Bismuth.  

- This is the only way a PoW coin can protect its network.  
  Pure GPU coins always are at the mercy of a nicehash or similarly rented hash attack.
- Hash/Watt of fpgas and asic is way better han GPUs, so you have better efficiency and more hash, a more secure network with more resources needed to take over.

This is only true if the mining equipment is largely available.  
It's not when a single op has thousands of custom proprietary hardware. 

Next step will be introducing **several mining channels**, so that everyone has a fair chance to mine, reach profitability, and contribute to the network safety.

This would also allow for faster algo changes should a similar situation arise again.
 

# FAQ

## Fork block/Date?

Block #854660.  
Means around Monday October 8, 14h UTC

## I'm a miner, what should I do?
Update your miners with compatible miners before the fork.  
The pools have been warned in priority, they should provide an updated miner before the fork.

## I run a node, what should I do?
Update your node with version 4.2.7.0 or a later one, asap.  
If you don't, after the fork block your node will be kicked out of the official network.

## I run a hypernode, what should I do?
Update your node with version 4.2.7.0 or a later one, asap.  
If you don't, after the fork block your node will be kicked out of the official network, and your HN will not work properly.    
Next HN required update - To be announced - will not work with older nodes.

## I'm a FPGA dev and spent 1 month working on BIS, for nuts?
Blame the greedy solo miner who took 60% + of the hash with huge fpga mining op.    
That was a threat we can not ignore.  
On the mid and long term, we will kinda re-introduce legacy bismuth mining, your work won't be lost. 

## Where can I find a tech description of the new algo?
See heavy3_mining_algo.pdf and this repo https://github.com/bismuthfoundation/mining-algos

## What is that "Junction Noise" file at startup?
The new memory heavy algorithm relies on a big file.  
This file is generated once at node start if it does not exists yet.    
This will need about 3 minutes, only once.
