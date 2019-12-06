from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def dataReceived(self, data):
        print(f"Sunucu mesajı: {data.decode('UTF-8')}")
        self.transport.loseConnection()

    def connectionMade(self):
        self.transport.write("Hello world".encode("UTF-8"))

class EchoFactory(protocol.ClientFactory):
    def clientConnectionFailed(self, connector, reason):
        print("Bağlantı başarısız")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Bağlantı koptu")
        reactor.stop()

    def buildProtocol(self, addr):
        return EchoClient()

reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()