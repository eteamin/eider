import json

from twisted.internet import reactor, protocol, error
from twisted.protocols import basic
from twisted.python import failure


from eider.utils import generate_uuid

connectionDone = failure.Failure(error.ConnectionDone())
connectionDone.cleanFailure()


class EiderProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients[generate_uuid()] = self.transport

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        self._distribute(data)

    def alive(self, payload=None):
        resp = {
            "alive": True
        }
        self._talk_back(json.dumps(resp))

    def get_all_users(self, payload=None):
        pass

    def _talk_back(self, data):
        self.transport.write(data.encode("utf-8"))

    def _de_jsonize(self, data):
        return json.loads(data.decode("utf-8"))

    def _distribute(self, data):
        _data = self._de_jsonize(data)
        method = getattr(self, _data.get("operation"))
        method(_data.get("payload"))


class EiderFactory(protocol.Factory):
    def __init__(self):
        self.clients = dict()

    def buildProtocol(self, addr):
        return EiderProtocol(self)


reactor.listenTCP(0, EiderFactory())
reactor.run()
