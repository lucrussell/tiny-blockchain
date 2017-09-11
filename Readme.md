# Tiny Blockchain

This is a port of [snakecoin](https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173) to use Docker and Python 3. All credit to [@aunyks](https://github.com/aunyks) and [https://github.com/zacanger](https://github.com/zacanger) who wrote the originals.

The idea is a toy Python blockchain to be used as a playground for experimentation.

This version adds the following to the original:
    
    * Python 3
    * [Falcon](http://falcon.readthedocs.io/en/stable/index.html) Web Framework
    * docker-compose to more easily run multiple nodes

## Usage

Start everything:

    docker-compose up

Add some transactions:

    curl "localhost:5001/transaction" \
         -H "Content-Type: application/json" \
         -d '{"from": "alice", "to":"bob", "amount": 3}'; \
    curl "localhost:5001/transaction" \
         -H "Content-Type: application/json" \
         -d '{"from": "alice", "to":"pete", "amount": 5}'; \
    curl "localhost:5002/transaction" \
         -H "Content-Type: application/json" \
         -d '{"from": "jeff", "to":"joe", "amount": 5}'; \
    curl "localhost:5001/mine"; \
    curl "localhost:5002/mine"; \
    curl "localhost:5002/mine"

`node1` has the longest chain.

Check the output, it should be the same on each node:

    curl localhost:5001/blocks | jq
    curl localhost:5002/blocks | jq
    curl localhost:5003/blocks | jq
