# Bismuth Mining Evolution

On October 8, 2018 (block height 854,660) a new and novel mining algorithm was introduced on the Bismuth network.

Before the new mining algorithm was introduced the distribution of the hashrate among the pools was as shown below:  
<img src="pools-854660.jpg" width="500" alt="Pools before the fork">  

It is believed that a large portion of the hashrate by Pool 4 was contributed by an FPGA miner.

A few days after the new mining algorithm was introduced the distribution of the hashrate among the pools was as shown below:  
<img src="pools-863318.jpg" width="500" alt="Pools after the fork">  

The difficulty plot before and after the hardfork is shown in the plot below:   
<img src="diffhist-hf.png" width="500" alt="Diff before and after hf">  

Since it was expected that about 50% of the hashrate would disappear after the hardfork, because of the new, memory intensive algorithm, a difficulty drop down to 108.9 was hard-coded into the node. As seen from the plot above, it took about 6 days (9000 blocks) before the difficulty level stabilized at 111.0. This level is more or less the same as before the hardfork. It is believed that the 40-50% hashrate which was previously provided by the FPGAs, was compensated by GPU miners (new or revious miners which had left) returning to Bismuth.
