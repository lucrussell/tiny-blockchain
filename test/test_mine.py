import datetime
import json
import unittest

from tinyblockchain.model import State, Block
from tinyblockchain.resources.blocks import BlocksResource


class TestApp(unittest.TestCase):

    def test_get_blocks(self):
        blockchain = [Block(0, datetime.datetime.now(), {
            "proof-of-work": 9,
            "transactions": None
        }, "0")]

        state = State('test', blockchain, [], [], True)

        blocks_resource = BlocksResource(state)
        response = MockResponse()
        blocks_resource.on_get(None, response)
        result = json.loads(response.body)
        self.assertEquals(0, result[0].get('index'))


class MockResponse(object):
    def __init__(self):
        self.body = None
