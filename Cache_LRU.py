from llist import dllist, dllistnode
from Components import *
import GlobalVar as gl

class Cache_LRU:
    blocks_num = 4
    n_associativity = 1
    def __init__(self, ram: Ram):
        self.ram = ram
        self.policy = "LRU"
        self.sets_num = gl.get_value('sets_num')

        self.cache_blocks = [dllist() for i in range(self.sets_num)]
        self.cache_dict = [{} for i in range(self.sets_num)]

        self.capacity_in_set = self.sets_num*[self.n_associativity]
        self.capacity = int(DataBlock.size/8)

        self.write_hit = 0
        self.write_miss = 0
        self.read_hit = 0
        self.read_miss = 0


    def setDouble(self, address: Address, value):

        cnt_index = address.getIndex()
        cnt_tag = address.getTag()
        cnt_offset = address.getOffset()


        cnt_set = self.cache_blocks[cnt_index]
        cnt_set_dict = self.cache_dict[cnt_index]


        if cnt_tag in cnt_set_dict.keys():
            self.write_hit += 1
            cnt_node = cnt_set_dict[cnt_tag]
            for node in cnt_set:
                if(cnt_node == node):
                    node[1].blockdata[cnt_offset] = value
        else:
            ram_block = self.ram.getBlock(address)
            self.write_miss += 1
            if(self.capacity_in_set[cnt_index] > 0):
                cnt_set.appendright(dllistnode([address, ram_block]))
                cnt_set_dict[cnt_tag] = cnt_set.nodeat(len(cnt_set)-1)
                self.capacity_in_set[cnt_index] -= 1
            else:
                self.setBlock(address, ram_block)


    def getDouble(self, address: Address) -> float:
        cnt_index = address.getIndex()
        cnt_tag = address.getTag()
        cnt_offset = address.getOffset()
        cnt_set = self.cache_blocks[cnt_index]
        cnt_set_dict = self.cache_dict[cnt_index]

        if cnt_tag in cnt_set_dict.keys():
            self.read_hit += 1

            found_node = cnt_set_dict[cnt_tag]
            removed_node = cnt_set.remove(found_node)
            cnt_set.appendright(removed_node)
            cnt_set_dict[cnt_tag] = cnt_set.nodeat(len(cnt_set)-1)
            return removed_node[1].block_data[cnt_offset]
        else:
            ram_block = self.ram.getBlock(address)
            self.read_miss += 1
            if(self.capacity_in_set[cnt_index] > 0):
                cnt_set.appendright(dllistnode([address, ram_block]))
                cnt_set_dict[cnt_tag] = cnt_set.nodeat(len(cnt_set)-1)
                self.capacity_in_set[cnt_index] -= 1
                
            else:
                self.setBlock(address, ram_block)
            return ram_block.block_data[cnt_offset]

    def setBlock(self, address: Address, datablock):
        cnt_index = address.getIndex()
        cnt_set = self.cache_blocks[cnt_index]
        cnt_set_dict = self.cache_dict[cnt_index]

        front_node = cnt_set.popleft()
        front_node_tag = front_node[0].getTag()

        if front_node_tag in cnt_set_dict: 
            del cnt_set_dict[front_node_tag]
        
        cnt_set.appendright(dllistnode([address, datablock]))
        cnt_set_dict[address.getTag()] = cnt_set.nodeat(len(cnt_set)-1)


    def getBlock(self, address: Address):
        cnt_index = address.getIndex()
        return self.cache_blocks[cnt_index][1]



