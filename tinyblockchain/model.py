import hashlib as hasher


class State(object):
    def __init__(self, miner_address,
                 blockchain,
                 peer_nodes,
                 node_transactions,
                 mining):
        self.miner_address = miner_address
        self.blockchain = blockchain
        self.peer_nodes = peer_nodes
        self.node_transactions = node_transactions
        self.mining = mining


class Block(object):
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        block = str(self.index) + str(self.timestamp) + str(self.data) + str(
            self.previous_hash)
        sha.update(block.encode('utf-8'))
        return sha.hexdigest()

    def __str__(self):
        return "Block <%s>: %s" % (self.hash, self.data)
