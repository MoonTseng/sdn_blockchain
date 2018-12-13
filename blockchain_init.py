import hashlib as hasher
import datetime as date

class Block:
#initialize blockchain
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    #Encryption of data on the block
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index)+str(self.timestamp)+str(self.data)+str(self.previous_hash))
        return sha.hexdigest()


def create_genesis_block():
        #Create a creation block and initialize it
        return Block(0, date.datetime.now(), {"POW": 9,"transaction": None}, "0")


def next_block(last_block):
       #Generate the next block
        this_index = last_block.index+1
        this_timestamp = date.datetime.now()
        this_data = "Hey! This is block "+str(this_index)
        this_hash = last_block.hash
        return Block(this_index, this_timestamp, this_data, this_hash)
