from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


class EiderProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        pass


class EiderFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return EiderProtocol(self)


endpoints.serverFromString(reactor, "tcp:1025").listen(PubFactory())
reactor.run()
