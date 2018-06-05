import json

from twisted.trial import unittest
from twisted.test import proto_helpers

from eider.handler.factory import EiderFactory


class TestSimpleConnection(unittest.TestCase):
    def setUp(self):
        factory = EiderFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, payload, expected):
        self.proto.dataReceived(payload)
        self.assertEqual(self.tr.value(), bytes(expected))

    def test_echo(self):
        payload = json.dumps({
            "operation": "echo",
            "payload": None
        }).encode("utf-8")
        return self._test(payload, True)


if __name__ == '__main__':
    unittest.main()
