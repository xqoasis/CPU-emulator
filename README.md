# CPU-emulator
A CPU emulator capable of modelling a simplified memory hierarchy

## Introduction:
An emulator for a CPU with physical memory addressing and a single-level cache.

It includes: 
- datablock: A block of data stored in cache.
- address: A memory address. Which includes tag, index, offset
- ram: Large enough to store all cache missed data
- Cache: There are FIFO policy cache, LRU policy cache and random policy cache. I devide them into 3 different classes.
- CPU: To load, store, add, muliply data.

## Instructions:
- Environment: Python 3.11.2 
- You need install `argparse`, `math`, `llist`
- You can change arguments by command line args:
```
-c : The size of the cache in bytes (default: 65,536)
-b : The size of a data block in bytes (default: 64)
-n : The n-way associativity of the cache. -n 1 is a direct-mapped cache. (default: 2)
-r : The replacement policy. Can be random, FIFO, or LRU. (default: LRU)
-a : The algorithm to simulate. Can be daxpy (daxpy product), mxm (matrix-matrix multiplication), mxm block (mxm with blocking). (default: mxm block).
-d : The dimension of the algorithmic matrix (or vector) operation. -d 100 would result in a 100 × 100 matrix-matrix multiplication. (default: 480)
-p : Enables printing of the resulting “solution” matrix product or daxpy vector after the emulation is complete. Elements should be read in emulation mode (e.g., using your loadDouble method), so as to assess if the emulator actually produced the correct solution.(default: 0, means not print)
-f : The blocking factor for use when using the blocked matrix multiplication algorithm. (default: 32)
```
- Input and output example:
```
INPUTS=================================================
Ram Size =                     5529600 bytes
Cache Size =                   32768 bytes
Block Size =                   64 bytes
Total Blocks in Cache =        512
Associativity =                32
Number of Sets =               16
Replacement Policy =           LRU
Algorithm =                    mxm_block
MXM Blocking Factor =          32
```
```
RESULTS=================================================
Instruction count = 449971200
Read hits =         223747200
Read misses =       892800
Read miss rate =    0.40%
Write hits =        4060800
Write misses =      86400
Write miss rate =   2.08%
```
- Example command line run:
```
python cache-sim.py -c 32768 -n 16
```
- Correctness check: run instruction
```
python cache-sim.py -d 9 -a daxpy -p 1
python cache-sim.py -d 9 -a mxm -p 1
python cache-sim.py -d 9 -a mxm_block -f 3 -p 1
```

## Shortcomming
- Python, as an interpreted language, has comparatively slow running speed. I can use cpython to compile Python code into bytecode before interpreting it, then to increase the speed. However, currently the average time of running a 512 x 512 tiled MXM algorithm is 10 mins. Therefore, I didn't use it. Besides, the more and easy way to speed up is to use C++ for programming.
- I didn't use numpy for my arrays. This package can also speed up the program.
- The variables and some methods of different caches are the same. It is better to implement a `Cache` class which receive the user determined replacement policy as an input, then behave differently.