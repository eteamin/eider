import json
from json.decoder import JSONDecodeError

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor, error
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
        # TODO: Handle this
        pass

    # noinspection PyUnusedLocal
    def alive(self, payload=None):
        resp = {
            "alive": True
        }
        self.transfer(resp)

    def transfer(self, payload, to=None):
        if not to:
            to = self.transport

        to.write(json.dumps(payload).encode("utf-8"))

    # noinspection PyUnusedLocal
    def get_all_users(self, payload=None):
        resp = []
        for k, v in self.factory.clients.items():
            resp.append(k)
        resp = {
            "users": resp
        }
        self.transfer(resp)

    def deliver_message(self, payload):
        # # Ack
        # resp = {
        #     "ok": True
        # }
        # self.transfer(resp)

        # Deliver the message
        to = self.factory.clients.get(payload["receiver"])

        message = {
            "text": payload.get("text")
        }
        self.transfer(message, to)

    # noinspection PyMethodMayBeStatic
    def load(self, data):
        try:
            return json.loads(data.decode("utf-8"))
        except (JSONDecodeError, UnicodeDecodeError):
            return {}

    def _digest_incoming_data(self, data):
        _data = self.load(data)
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
    factory.clients = dict()

    # noinspection PyUnresolvedReferences
    reactor.listenTCP(8585, factory)

    # noinspection PyUnresolvedReferences
    reactor.run()
