from Components import *
from random import randrange

class Cache_Random:
	blocks_num = 4
	n_associativity = 1
	def __init__(self, ram: Ram):
		self.ram = ram
		self.policy = "random"
		self.sets_num = gl.get_value('sets_num')
		self.cache_blocks = [self.n_associativity*[None] for i in range(self.sets_num)]

		self.write_hit = 0
		self.write_miss = 0
		self.read_hit = 0
		self.read_miss = 0

	def setDouble(self, address: Address, value):
		cnt_index = address.getIndex()
		cnt_tag = address.getTag()
		cnt_offset = address.getOffset()

		cnt_set = self.cache_blocks[cnt_index]
		is_cache_block = False

		none_block_num = -1

		for i in range(self.n_associativity):
			cnt_block = cnt_set[i]		
			if cnt_block == None:
				none_block_num = i
			else:
				if cnt_block[0].getTag() == cnt_tag:
					self.write_hit += 1
					is_cache_block = True
					cnt_set[i][0] = address
					cnt_set[i][1].block_data[cnt_offset] = value
					break
		
		if is_cache_block == False: #block is not in cache, in RAM
			ram_block = self.ram.getBlock(address)
			self.write_miss += 1
			if none_block_num != -1: 
				cnt_set[none_block_num] = [address, ram_block]
			else:
				self.setBlock(address, ram_block)

	def getDouble(self, address: Address):
		cnt_index = address.getIndex()	
		cnt_tag = address.getTag()
		cnt_offset = address.getOffset()

		cnt_set = self.cache_blocks[cnt_index]

		is_cache_block = False
		none_block_num = -1
	
		for i in range(self.n_associativity):
			cnt_block = cnt_set[i]		
			if cnt_block == None:
				none_block_num = i
			else:
				if cnt_block[0].getTag() == cnt_tag:
					self.read_hit += 1
					return cnt_block[1].block_data[cnt_offset]

		if is_cache_block == False:
			ram_block = self.ram.getBlock(address)
			if none_block_num != -1:
				cnt_set[none_block_num] = [address, ram_block]
			else:
				self.read_miss += 1
				self.setBlock(address, ram_block)
			return ram_block.block_data[cnt_offset]

	def setBlock(self, address: Address, datablock):
		cnt_index = address.getIndex()
		in_set_index = randrange(self.n_associativity)
		self.cache_blocks[cnt_index][in_set_index] = [address, datablock]

	def getBlock(self, address: Address):
		cnt_index = address.getIndex()
		return self.cache_blocks[cnt_index][1]





