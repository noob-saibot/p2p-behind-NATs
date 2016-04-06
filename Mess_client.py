# -*- coding: utf-8 -*-
"""
Client for connecting p2p through NAT to Message server.
"""
# Created by Anton Alekseev, April 2016
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class ClientDatagramProtocol(DatagramProtocol):
    """
    Class describe protocol of handling UDP datagram.
    """
    def __init__(self, s_client='[True, "Client 911"]'):
        self.s_client = s_client

    def connectionRefused(self):
        """
        This method return information about connection status.
        """
        print "No one listening"
        if reactor.running:
            reactor.stop()

    def startProtocol(self):
        """
        This method describe information for starting protocol.
        """
        self.sendDatagram()

    def sendDatagram(self):
        """
        Request to Signal server about some client.
        """
        if self.s_client:
            self.transport.write(self.s_client, ('127.0.0.1', 4444))
        elif reactor.running:
            reactor.stop()

    def datagramReceived(self, datagram, host):
        """
        Sending some information to Message server.
        :param datagram: Incoming data.
        :param host: Address of transmitter.
        """
        print datagram
        datagram = repr(datagram).replace("'", '').split(':')[-2:]
        print 'Go to: ', ':'.join(datagram)
        datagram = datagram[0].split('(')[1].replace(')"', '').split(', ')
        self.transport.write('Hello Server', (datagram[0], int(datagram[1])))

if __name__ == '__main__':
    protocol = ClientDatagramProtocol()
    t = reactor.listenUDP(0, protocol)
    reactor.run()
