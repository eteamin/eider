from twisted.trial import unittest
from twisted.test import proto_helpers

from eider.handler.factory import EiderProtocol


class TestSimpleConnection(unittest.TestCase):
    def setUp(self):
        self.tr = proto_helpers.StringTransport()
        self.proto = EiderProtocol()
        self.proto.makeConnection(self.tr)

    def _test(self, operation, payload, expected):
        d = getattr(self.proto, operation)(payload)
        self.assertEqual(
            self.tr.value(),
            u'{} {}\r\n'.format(operation, payload).encode('utf-8')
        )
        self.tr.clear()
        d.addCallback(self.assertEqual, expected.encode("utf-8"))
        self.proto.dataReceived(u"{}\r\n".format(expected).encode('utf-8'))
        return d

    def test_echo(self):
        return self._test('echo', "hi", "hi")


if __name__ == '__main__':
    unittest.main()
