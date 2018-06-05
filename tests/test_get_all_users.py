import json

from twisted.trial import unittest

from tests import EiderTestCase


class GetUsersTestCase(EiderTestCase):

    def test_get_all_users(self):
        payload = json.dumps({
            "operation": "get_all_users",
            "payload": None
        }).encode("utf-8")

        self.protocol.onMessage(payload, False)
        resp = json.loads(self.transport.value().decode("utf-8"))
        self.assertEqual(len(resp.get('users')), 1)


if __name__ == '__main__':
    unittest.main()
