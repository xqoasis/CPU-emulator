import GlobalVar as gl

class DataBlock:
	size = 64
	def __init__(self, data):
		self.block_data = int(self.size/8)*[data]

class Address:
	def __init__(self, address):
		self.address = address 
		self.num_sets = gl.get_value("sets_num")

	def getOffset(self):
		return int(self.address % (DataBlock.size//8))

	def getTag(self):
		block_num = int(self.address/(DataBlock.size//8))
		return int(block_num/self.num_sets)

	def getIndex(self):
		block_num = int(self.address/(DataBlock.size//8))
		return int(block_num % self.num_sets)


class Ram:
	def __init__(self, blocks_num):
		self.blocks_num = blocks_num
		self.data = [DataBlock(None) for i in range(blocks_num)]

	def setBlock(self, address: Address, value):
		block_num = int(address.address/(DataBlock.size//8))
		block_offset = address.getOffset()
		self.data[block_num].block_data[block_offset] = value
		
	def getBlock(self, address: Address) -> DataBlock:
		block_num = int(address.address/(DataBlock.size//8))
		return self.data[block_num]

	
		


