from twisted.internet import reactor, protocol
class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
    def connectionMade(self):
        self.sendQuote()
    def sendQuote(self):
        self.transport.write(self.factory.quote.encode("UTF-8"))
    def dataReceived(self, data):
        print(f"Received quote: {data}")
        self.transport.loseConnection()


class QuoteClientFactory(protocol.ClientFactory):
    def __init__(self, quote):
        self.quote = quote
    def buildProtocol(self, addr):
        return QuoteProtocol(self)
    def clientConnectionFailed(self, connector, reason):
        print(f"connection failed: {reason.getErrorMessage()}")
        maybeStopReactor()
    def clientConnectionLost(self, connector, reason):
        print(f"connection lost: {reason.getErrorMessage()}")
        maybeStopReactor()


def maybeStopReactor():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()


quotes = [
    "You snooze you lose",
    "The early bird gets the worm",
    "Carpe diem",
    "Stars can not shine without darkness!"
]
quote_counter = len(quotes)
for quote in quotes:
    reactor.connectTCP('localhost', 8000, QuoteClientFactory(quote))
reactor.run()