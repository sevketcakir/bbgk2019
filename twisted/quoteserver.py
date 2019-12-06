from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol

class QuoteProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print(f"Aktif bağlantı sayısı: {self.factory.numConnections}")
        print(f"Gelen: {data.decode('UTF-8')}")
        print(f"Gönderilen: {self.getQuote()}")
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionMade(self):
        self.factory.numConnections += 1

    def __init__(self, factory):
        self.factory = factory

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0
    def buildProtocol(self, addr):
        return QuoteProtocol(self)

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps the doctor away".encode("UTF-8")


reactor.listenTCP(8000, QuoteFactory())
reactor.run()