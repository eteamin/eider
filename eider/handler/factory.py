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
        # TODO: Figure out a way to handle this
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        self._digest_incoming_data(data)

    def alive(self, payload=None):
        resp = {
            "alive": True
        }
        self._talk_back(json.dumps(resp))

    def send_message(self, payload):
        receiver = self.factory.clients.get(payload.get("receiver"))
        _payload = {
            "text": payload.get("text")
        }
        self._talk_back(json.dumps(_payload), receiver=receiver)

    def get_all_users(self, payload=None):
        resp = []
        for k, v in self.factory.clients.items():
            resp.append(k)
        resp = {
            "users": resp
        }
        self._talk_back(json.dumps(resp))

    def _talk_back(self, data, receiver=None):
        if receiver:
            receiver.write(data.encode("utf-8"))
        else:
            self.transport.write(data.encode("utf-8"))

    def _de_jsonize(self, data):
        return json.loads(data.decode("utf-8"))

    def _digest_incoming_data(self, data):
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
