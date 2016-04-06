# -*- coding: utf-8 -*-
"""
Message server for building p2p connect through NAT.
"""
# Created by Anton Alekseev, April 2016
import time

import stun
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import DatagramProtocol


class Twist(DatagramProtocol):
    """
    This class describe protocol of interaction between Message server and Clients.
    """
    def __init__(self, s_connect=False, s_thread=False):
        self.s_connect = s_connect
        self.s_thread = s_thread

    def datagramReceived(self, data, address):
        """
        Change s_connect in bool.
        :param data: Incoming data.
        :param address: Address of transmitter.
        """
        if data.startswith('Hello Server'):
            print data, address
        elif data.startswith('Empty'):
            self.s_connect = True

    def connectionSupport(self):
        """
        This method provide reserve of external port on external router
        or rewrite info about external port on Signal server.
        """
        self.transport.write('[True, "something"]', ('10.0.16.24', 4444))
        time.sleep(2)
        if self.s_connect:
            self.s_connect = False
            self.connectionSupport()
        else:
            self.sendDatagram('[False, "Client 911", %s]' % str(stun.get_ip_info()[1:]))
            self.connectionSupport()

    def startProtocol(self):
        """
        This method describe information for starting protocol.
        """
        self.sendDatagram('[False, "Client 911", %s]' % str(stun.get_ip_info()[1:]))
        reactor.callInThread(self.connectionSupport)

    def sendDatagram(self, docs, addr='127.0.0.1', port=4444):
        """
        :param docs: Data to transmitting.
        :param addr: Address of receiver.
        :param port: Port of receiver.
        """
        self.transport.write(docs, (addr, port))


if __name__ == '__main__':
    protocol = Twist()
    t = reactor.listenUDP(7777, protocol)
    reactor.run()
