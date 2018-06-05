import json
from twisted.trial import unittest

from tests import EiderTestCase


class AliveTestCase(EiderTestCase):

    def test_alive(self):
        payload = json.dumps({
            "operation": "alive",
            "payload": None
        }).encode("utf-8")
        expected = {
            "alive": True
        }
        self.protocol.onMessage(payload, False)
        self.assertEqual(json.loads(self.transport.value().decode("utf-8")), expected)


if __name__ == '__main__':
    unittest.main()
