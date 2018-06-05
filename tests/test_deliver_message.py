import json

from twisted.trial import unittest

from tests import EiderTestCase


class DeliverMessageTestCase(EiderTestCase):

    def setUp(self):
        super(DeliverMessageTestCase, self).setUp()

        # We need to get all users to find someone to talk to!
        payload = json.dumps({
            "operation": "get_all_users",
            "payload": None
        }).encode("utf-8")

        self.protocol.onMessage(payload, False)
        resp = json.loads(self.transport.value().decode("utf-8"))
        self.transport.clear()
        self.receiver = resp.get("users")[0]

    def test_send_message(self):
        message = {
            "text": "hello!",
            "receiver": self.receiver
        }
        payload = json.dumps({
            "operation": "deliver_message",
            "payload": message
        }).encode("utf-8")

        self.protocol.onMessage(payload, False)
        resp = json.loads(self.transport.value().decode("utf-8"))
        assert resp.get("text") == message.get("text")


if __name__ == '__main__':
    unittest.main()
