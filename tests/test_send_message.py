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

        # We need to get all users to have someone to talk to!
        payload = json.dumps({
            "operation": "get_all_users",
            "payload": None
        }).encode("utf-8")

        self.proto.dataReceived(payload)
        resp = json.loads(self.tr.value().decode("utf-8"))
        self.tr.clear()
        self.receiver = resp.get("users")[0]

    def test_send_message(self):
        message = {
            "text": "hello!",
            "receiver": self.receiver
        }
        payload = json.dumps({
            "operation": "send_message",
            "payload": message
        }).encode("utf-8")

        self.proto.dataReceived(payload)
        resp = json.loads(self.tr.value().decode("utf-8"))
        assert resp.get("text") == message.get("text")


if __name__ == '__main__':
    unittest.main()
