import json

from twisted.trial import unittest
from twisted.test import proto_helpers

from eider.handler.factory import EiderFactory


class EiderTestCase(unittest.TestCase):
    def setUp(self):
        factory = EiderFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_alive(self):
        payload = json.dumps({
            "operation": "alive",
            "payload": None
        }).encode("utf-8")
        expected = {
            "alive": True
        }
        self.proto.dataReceived(payload)
        self.assertDictEqual(json.loads(self.tr.value().decode("utf-8")), expected)


if __name__ == '__main__':
    unittest.main()
