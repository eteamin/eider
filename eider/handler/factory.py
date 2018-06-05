import json
from json.decoder import JSONDecodeError

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor, protocol, error
from twisted.protocols import basic
from twisted.python import failure


from eider.utils import generate_uuid

connectionDone = failure.Failure(error.ConnectionDone())
connectionDone.cleanFailure()


class EiderProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        self.factory.clients[generate_uuid()] = self.transport

    def onMessage(self, payload, isBinary):
        self._digest_incoming_data(payload)

    def onClose(self, wasClean, code, reason):
        self.factory.clients = dict()

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
        self.sendMessage(data.encode("utf-8"))

    def _de_jsonize(self, data):
        try:
            return json.loads(data.decode("utf-8"))
        except (JSONDecodeError, UnicodeDecodeError):
            return {}

    def _digest_incoming_data(self, data):
        _data = self._de_jsonize(data)
        if not _data:
            return
        try:
            method = getattr(self, _data.get("operation"))
        except AttributeError:
            return
        method(_data.get("payload"))


if __name__ == '__main__':
    factory = WebSocketServerFactory(u"ws://172.20.10.3:8585")
    factory.protocol = EiderProtocol

    reactor.listenTCP(8585, factory)
    reactor.run()
