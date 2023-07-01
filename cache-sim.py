from Components import *
from Cache_FIFO import *
from Cache_LRU import *
from Cache_RANDOM import *
import GlobalVar as gl
import argparse
import math

from llist import dllist, dllistnode

## Based on the descriptions in Patterson and Hennessey, Computer Organization and Design, 5th Edition, Chapters 5.3 - 5.4.
class CPU:
	def __init__(self, cache):
		self.cache = cache
		self.instruction_count = 0

	def storeDouble(self, address: Address, value):
		cnt_address = Address(address)
		self.cache.setDouble(cnt_address, value)
		# write through
		self.cache.ram.setBlock(cnt_address, value)
		self.instruction_count += 1
                
	def loadDouble(self, address):
		self.instruction_count += 1
		return self.cache.getDouble(Address(address))

	def multDouble(self, value1, value2):
		self.instruction_count += 1
		return value1 * value2

	def addDouble(self, value1, value2):
		self.instruction_count += 1
		return value1 + value2

def printInput(a, b, c, d, e, f, g, h, i, j):
    print("INPUTS=================================================")
    print("Ram Size =                     %d bytes" % (a))
    print("Cache Size =                   %d bytes" % (b))
    print("Block Size =                   %d bytes" % (c))
    print("Total Blocks in Cache =        %d" % (d))
    print("Associativity =                %d" % (e))
    print("Number of Sets =               %d" % (f))
    print("Replacement Policy =           %s" % (g))
    print("Algorithm =                    %s" % (h))
    print("MXM Blocking Factor =          %d" % (i))
    print("Matrix or Vector dimennsion =  %d" % (j))

def printOutput(a, b, c, d, e):
    print("RESULTS=================================================")
    print("Instruction count = %d" % (a))
    print("Read hits =         %d" % (b))
    print("Read misses =       %d" % (c))
    print("Read miss rate =    %.2f" % (100.0*c/(c + b)) + "%")
    print("Write hits =        %d" % (d))
    print("Write misses =      %d" % (e))
    print("Write miss rate =   %.2f" % (100.0*e/(d + e)) + "%")

     
if __name__ == "__main__":
    gl._init()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", default=65536, help="The size of the cache in bytes (default: 65,536)")
    parser.add_argument("-b", default=64, help="The size of a data block in bytes (default: 64)")
    parser.add_argument("-n", default=2, help="The n-way associativity of the cache. -n 1 is a direct-mapped cache. (default: 2)")
    parser.add_argument("-r", default='LRU', help="The replacement policy. Can be random, FIFO, or LRU. (default: LRU)")
    parser.add_argument("-a", default='mxm_block', help="The algorithm to simulate. Can be daxpy (daxpy product), mxm (matrix-matrix multiplication), mxm block (mxm with blocking). (default: mxm_block)")
    parser.add_argument("-d", default=480, help="The dimension of the algorithmic matrix (or vector) operation. -d 100 would result in a 100 × 100 matrix-matrix multiplication. (default: 480)")
    parser.add_argument("-p", default=0, help="Enables printing of the resulting “solution” matrix product or daxpy vector after the emulation is complete.")
    parser.add_argument("-f", default=32, help="The blocking factor for use when using the blocked matrix multiplication algorithm. (default: 32)")

    args = parser.parse_args()
    cache_size = int(args.c)
    block_size = int(args.b)
    associativity = int(args.n)
    policy = args.r
    test_type = args.a
    dimension = int(args.d)
    tiled_factor = int(args.f)
    print_flag = int(args.p)

    # initialize components according to input
    if policy == "random":
        print("random replacement policy")
        MyCacheClass = Cache_Random
    elif policy == "FIFO":
        print("FIFO replacement policy")
        MyCacheClass = Cache_FIFO
    else:
        print("LRU replacement policy")
        # default
        MyCacheClass = Cache_LRU

    DataBlock.size = block_size
    MyCacheClass.n_associativity = associativity
    MyCacheClass.blocks_num = cache_size / block_size
    if test_type != "daxpy":
        ram_block_num = math.ceil(dimension*dimension*3*8/block_size)
    else:
        ram_block_num = math.ceil(3*dimension*8/block_size)

    
    gl.set_value('sets_num', int(cache_size/(associativity*block_size)))
    gl.set_value('associativity', associativity)
    myRam = Ram(ram_block_num)
    myCache = MyCacheClass(myRam)
    myCpu = CPU(myCache)


    if test_type == "daxpy":
        print("daxpy test")
        # Construct arrays of Addresses for length = n (input dimension)
        sz = 1 
        n = dimension
        a = list(range(0, n*sz, 1))
        b = list(range(n, 2*n*sz, 1))
        c = list(range(2*n*sz, 3*n*sz, 1))

        # Initialize some dummy values
        for i in range(n):
            myCpu.storeDouble(address=a[i], value=i)
            myCpu.storeDouble(address=b[i], value=2*i)
            myCpu.storeDouble(address=c[i], value=0)

        # Put a random 'D' value into a register
        register0 = 3
        for i in range(n):
            register1 = myCpu.loadDouble(a[i])
            register2 = myCpu.multDouble(register0, register1)
            register3 = myCpu.loadDouble(b[i])
            register4 = myCpu.addDouble(register2, register3)
            myCpu.storeDouble(address=c[i], value=register4)

        print("\n\n")
        printInput(myRam.blocks_num * DataBlock.size, myCache.blocks_num * DataBlock.size, DataBlock.size, myCache.blocks_num, myCache.n_associativity, myCache.sets_num, myCache.policy, test_type, tiled_factor, dimension)
        printOutput(myCpu.instruction_count, myCache.read_hit, myCache.read_miss, myCache.write_hit, myCache.write_miss)
        print("\n\n")
        if print_flag == 1:
            result = []
            for address in c:
                temp_register = myCpu.loadDouble(address)
                result.append(temp_register)
            print(result)

    elif(test_type == 'mxm'):
        print("regular mxm test")
        n = dimension

        a = list(range(0, n*n, 1))
        b = list(range(n*n, 2*n*n, 1))
        c = list(range(2*n*n, 3*n*n, 1))
        for i in range(n*n):
            myCpu.storeDouble(address = a[i], value = i)
            myCpu.storeDouble(address = b[i], value = 2*i)
            myCpu.storeDouble(address = c[i], value = 0)
        for i in range(n):
            for j in range(n):
                register0=0
                for k in range(n):
                    register1 = myCpu.loadDouble(a[i*n+k])
                    register2 = myCpu.loadDouble(b[k*n+j])
                    register3 = myCpu.multDouble(register1, register2)
                    register0 = myCpu.addDouble(register0, register3)
                myCpu.storeDouble(address = c[i*n + j], value = register0)

        print("\n\n")
        printInput(myRam.blocks_num * DataBlock.size, myCache.blocks_num * DataBlock.size, block_size, myCache.blocks_num, myCache.n_associativity, myCache.sets_num, myCache.policy, test_type, tiled_factor, dimension)
        printOutput(myCpu.instruction_count, myCache.read_hit, myCache.read_miss, myCache.write_hit, myCache.write_miss)
        print("\n\n")
        if print_flag == 1:
            result = []
            for address in c:
                temp_register = myCpu.loadDouble(address)
                result.append(temp_register)
            print(result)
    else:
        print("tiled mxm test")
        n = dimension
        #d = zero_matrix(n,n)
        a = list(range(0, n*n, 1))
        b = list(range(n*n, 2*n*n, 1))
        c = list(range(2*n*n, 3*n*n, 1))

        temp_c = 0
        for i in range(n*n):
            myCpu.storeDouble(address = a[i], value = i)
            myCpu.storeDouble(address = b[i], value = 2*i)
            myCpu.storeDouble(address = c[i], value = 0)


        for kk in range(0, n, tiled_factor):
            for jj in range(0, n, tiled_factor):
                for i in range(n):
                    for j in range(jj, jj + tiled_factor):
                        register0 = myCpu.loadDouble(c[i*n + j])
                        for k in range(kk, kk + tiled_factor):
                            register1 = myCpu.loadDouble(a[i*n + k])
                            register2 = myCpu.loadDouble(b[k*n + j])
                            register3 = myCpu.multDouble(register1, register2)
                            register0 = myCpu.addDouble(register0, register3)

                        myCpu.storeDouble(address = c[i*n + j], value = register0)

        print("\n\n")
        printInput(myRam.blocks_num * DataBlock.size, myCache.blocks_num * DataBlock.size, block_size, myCache.blocks_num, myCache.n_associativity, myCache.sets_num, myCache.policy, test_type, tiled_factor, dimension)
        printOutput(myCpu.instruction_count, myCache.read_hit, myCache.read_miss, myCache.write_hit, myCache.write_miss)
        print("\n\n")
        if print_flag == 1:
            result = []
            for address in c:
                temp_register = myCpu.loadDouble(address)
                result.append(temp_register)
            print(result)



