import json

from twisted.trial import unittest
from twisted.test import proto_helpers

from tests import MyProtocolFactory


class EiderTestCase(unittest.TestCase):
    def setUp(self):
        factory = MyProtocolFactory()
        protocol = factory.buildProtocol(None)
        transport = proto_helpers.StringTransport()
        protocol.makeConnection(transport)
        self.protocol, self.transport = protocol, transport

    def test_get_all_users(self):
        payload = json.dumps({
            "operation": "get_all_users",
            "payload": None
        }).encode("utf-8")

        self.proto.dataReceived(payload)
        resp = json.loads(self.tr.value().decode("utf-8"))
        self.assertEqual(len(resp.get('users')), 1)


if __name__ == '__main__':
    unittest.main()
