import json


class BlocksResource(object):
    def __init__(self, state):
        self.state = state

    def on_get(self, req, resp, **params):
        print("BlocksResource called")
        chain_to_send = []
        # Return chain as dictionary
        for i in range(len(self.state.blockchain)):
            block = self.state.blockchain[i]
            chain_to_send.append({
                "index": block.index,
                "timestamp": str(block.timestamp),
                "data": block.data,
                "hash": block.hash
            })
        resp.body = json.dumps(chain_to_send)
