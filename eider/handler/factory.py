from twisted.internet import reactor, protocol, endpoints, error
from twisted.protocols import basic
from twisted.python import failure
from twisted.internet import defer


from eider.utils import generate_uuid

connectionDone = failure.Failure(error.ConnectionDone())
connectionDone.cleanFailure()


class EiderProtocol(basic.LineReceiver):
    def __init__(self, factory=None):
        self.factory = factory
        self.results = []

    def connectionMade(self):
        if self.factory:
            self.factory.clients[generate_uuid()] = self.transport

    def connectionLost(self, reason=connectionDone):
        if self.factory:
            self.factory.clients.remove(self)

    def lineReceived(self, line):
        d = self.results.pop(0)
        d.callback(line)

    def _sendOperation(self, op, payload):
        d = defer.Deferred()
        self.results.append(d)
        line = u"{} {}".format(op, payload).encode('utf-8')
        self.sendLine(line)
        return d

    def echo(self, payload):
        return self._sendOperation("echo", payload)


class EiderFactory(protocol.Factory):
    def __init__(self):
        self.clients = dict()

    def buildProtocol(self, addr):
        return EiderProtocol(self)


endpoints.serverFromString(reactor, "tcp:1025").listen(EiderFactory())
reactor.run()
