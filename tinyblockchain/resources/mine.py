import json
from datetime import datetime

import requests

from tinyblockchain.model import Block


class MineResource(object):
    def __init__(self, state):
        self.state = state

    def on_get(self, req, resp, **params):
        self.consensus()

        # Get the last proof of work
        last_block = self.state.blockchain[len(self.state.blockchain) - 1]
        last_proof = last_block.data['proof-of-work']
        # Find the proof of work for the current block being mined
        # Note: The program will hang here until a new
        #       proof of work is found
        proof = self.proof_of_work(last_proof)
        # Once we find a valid proof of work, we know we can mine a block so
        # we reward the miner by adding a transaction
        self.state.node_transactions.append(
            {"from": "network", "to": self.state.miner_address, "amount": 1}
        )
        # Now we can gather the data needed to create the new block
        new_block_data = {
            "proof-of-work": proof,
            "transactions": list(self.state.node_transactions)
        }
        new_block_index = last_block.index + 1
        new_block_timestamp = datetime.now()
        last_block_hash = last_block.hash
        # Empty transaction list
        self.state.node_transactions[:] = []
        # Now create the new block!
        mined_block = Block(
            new_block_index,
            new_block_timestamp,
            new_block_data,
            last_block_hash
        )
        self.state.blockchain.append(mined_block)
        # Let the client know we mined a block
        resp.body = json.dumps({
            "index": new_block_index,
            "timestamp": str(new_block_timestamp),
            "data": new_block_data,
            "hash": last_block_hash
        })

    def proof_of_work(self, last_proof):
        # Create a variable that we will use to find our next proof of work
        incrementor = last_proof + 1
        # Keep incrementing until it's equal to a number divisible
        # by 9 and the proof of work of the previous block in the chain
        while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
            incrementor += 1
        # Once that number is found, we can return it as a proof of our work
        return incrementor

    def consensus(self):
        # Get the blocks from other nodes
        other_chains = self.find_new_chains()
        print("Found other {} chains".format(len(other_chains)))
        # If our chain isn't longest, then we store the longest chain
        longest_chain = self.state.blockchain
        for node, chain in other_chains.items():
            if len(longest_chain) < len(chain):
                print(
                    "Replacing blockchain with chain from node: {} ".format(
                        node))
                longest_chain = chain
        # If the longest chain isn't ours, then we stop mining and set
        # our chain to the longest one
        self.state.blockchain = longest_chain

    def find_new_chains(self):
        # Get the blockchains of every other node
        other_chains = {}
        print("Searching peer nodes: {} ".format(self.state.peer_nodes))
        for node_url in self.state.peer_nodes:
            chain = None
            try:
                chain = requests.get(node_url + "/blocks")
            except:
                print('Unable to retrieve chain from peer {}'.format(
                    node_url))
                print('Chain: '.format(chain))
            if chain:
                node_chain = []
                # Chains will be returned as json, convert them to objects
                c = json.loads(chain.content.decode('utf-8'))
                for block in c:
                    node_chain.append(Block(
                        block['index'],
                        block['timestamp'],
                        block['data'],
                        block['hash']))
                other_chains[node_url] = node_chain
        return other_chains
