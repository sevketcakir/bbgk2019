from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print(f"Mesaj({self.transport.getPeer()}): {data}")
        self.transport.write(data)

    def connectionMade(self):
        print(self.transport.getPeer())


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()