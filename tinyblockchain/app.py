"""

Usage:
    tinyblockchain [options]

Options:
    --config-file=<file>        Config file path.
"""
import datetime
import os
import uuid

import falcon
import yaml
from docopt import docopt
from gunicorn.app.base import BaseApplication

from tinyblockchain.model import Block, State
from tinyblockchain.resources import blocks
from tinyblockchain.resources import mine
from tinyblockchain.resources import transaction


class ApiServer(falcon.API):

    def __init__(self, config):
        super().__init__()

        # Random address of the owner of this node
        miner_address = str(uuid.uuid4())

        # Manually construct a block with index zero and arbitrary
        # previous hash
        genesis_block = Block(0, datetime.datetime.now(), {
            "proof-of-work": 9,
            "transactions": None
        }, "0")

        # This node's blockchain copy
        blockchain = [genesis_block]
        peer_nodes = config['node']['peer_nodes']

        state = State(miner_address, blockchain, peer_nodes, [], True)
        self.add_route('/transaction', transaction.TransactionResource(state))
        self.add_route('/mine', mine.MineResource(state))
        self.add_route('/blocks', blocks.BlocksResource(state))


class GunicornApp(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app

        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def configure(filename):
    if os.path.exists(filename) is False:
        raise IOError("{0} does not exist".format(filename))

    with open(filename) as config_file:
        config_data = yaml.load(config_file)

    return config_data


def main(arguments=None):
    if not arguments:
        arguments = docopt(__doc__)
    config = configure(arguments['--config-file'])
    app = ApiServer(config)
    GunicornApp(app, config['gunicorn']).run()


if __name__ == "__main__":
    main()
