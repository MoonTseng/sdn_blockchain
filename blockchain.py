from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
import blockchain_init
from blockchain_init import Block
from blockchain_init import create_genesis_block
from blockchain_init import next_block



node = Flask(__name__)

#strore the transaction in a node
transaction_of_current_node = []

#we firstly define a miner address,it's just a random address
minier_address = "0x2f3a5962357058e89fd6c86890d3d0b22b8983b1"

#Create initial blocks and add them to the blockchain
blockchain = []
blockchain.append(create_genesis_block())

#store ervey url of nodes in network
#node communicates with other node by url
p2pNodes = []
#a variable to define whether the node is mining
mining_runnnig = True

@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        #When met a new POST request, we extract a transaction data
        new_transaction = request.get_json()
        #Then we will append it to a list
        transaction_of_current_node.append(new_transaction)
        #The current node has got the transaction this this data
        #then print it in console
        print "New transaction"
        print "From: {}".format(new_transaction['from'])
        print "To: {}".format(new_transaction['to'])
        print "Amount: {}\n".format(new_transaction['amount'])
        return "Transaction has been submitted successful\n"

#now we have recorded the transaction in every node

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    #covert our blocks into dictionary
    blocklist = ""
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        assembled = json.dumps({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        })
        #Send it to other nodes who requested
    if blocklist =="":
        blocklist = assembled
    else:
        blocklist += assembled
    return blocklist

def find_new_chains():
    #Get the blockchain of every
    #other node
    other_chains = []
    for node_url in p2pNodes:
        #Get their chain by a GET request
        block = requests.get(node_url + "/blocks").content
        #Convert the Json Object to a Python dictionaries
        block = json.loads(block)
        #Add it to our list
        other_chains.append(block)
    return other_chains

def consensus_process():
    #Get block from other nodes
    other_chains = find_new_chains()
    #If our chain isn't longest,
    #then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain)<len(chain):
            chain = longest_chain
    #If longest chain isn't ours
    #then we set our chain as longest_chain
    blockchain = longest_chain


#The we should implement a consensus algorithms like POW(proof of work)
def proof_of_work(last_result):
    #we should define a var to find the result of proof_of_work
    current_result = last_result +1
    #Because we want to simulate the mechanism of proof_of_work
    #So we can define a number when it can be divided by 14
    #Once we find the number and we return it
    while not(current_result % 14 == 0 and current_result % last_result == 0):
        current_result +=1
    return current_result



@node.route('/mining', methods = ['GET'])
def mining():
    #Get the last proof of work result of block
    last_block = blockchain[len(blockchain) - 1]
    last_result = last_block.data['POW']
    #Find the proof of work for the  current block which is being mined
    #PLease be care !!!!: this progream will hang out until it find the result
    pow = proof_of_work(last_result)
    #once we find a correct proof of work
    #we know we can be mining so we will reward the miner by adding a transaction
    transaction_of_current_node.append({
     "from": "network",
      "to": minier_address,
      "amount": 1
    })
    #Now we gather the data to create the new block
    new_block_data = {
       "POW": pow,
       "transactions": list(transaction_of_current_node)
    }
    new_block_index = last_block.index+1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    #make the transaction list empty
    transaction_of_current_node[:] = []
    #create new block
    mining_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    blockchain.append(mining_block)
    return json.dumps(
      {
       "index": new_block_index,
       "timestamp": str(new_block_timestamp),
       "data": new_block_data,
       "hash": last_block_hash
      }
    )+"\n"
node.run()
