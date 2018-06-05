from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.trial import unittest
from twisted.test import proto_helpers

from eider.handler.factory import EiderProtocol


class MyProtocolFactory(WebSocketServerFactory):
    def __init__(self):
        WebSocketServerFactory.__init__(self, "ws://127.0.0.1:8081")

    def buildProtocol(self, addr):
        protocol = EiderProtocol()
        protocol.factory = self
        return protocol


class EiderTestCase(unittest.TestCase):

    def setUp(self):
        factory = MyProtocolFactory()
        protocol = factory.buildProtocol(None)
        transport = proto_helpers.StringTransport()
        protocol.makeConnection(transport)
        self.protocol, self.transport = protocol, transport

    def tearDown(self):
        for call in [
            self.protocol.autoPingPendingCall,
            self.protocol.autoPingTimeoutCall,
            self.protocol.openHandshakeTimeoutCall,
            self.protocol.closeHandshakeTimeoutCall,
        ]:
            if call is not None:
                call.cancel()
