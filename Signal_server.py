# -*- coding: utf-8 -*-
"""
Signal server for building p2p connect through NAT
"""
# Created by Anton Alekseev, April 2016
import logging

from twisted.internet import defer, reactor
from twisted.internet import protocol
from twisted.internet.defer import returnValue


class Twist(protocol.Protocol):
    """
    This class describe protocol of interaction between Signal server and Clients.
    """
    def __init__(self, addr='127.0.0.1'):
        self.addr = addr

    def datagramReceived(self, data, address):
        """
        This method calling s_response if deferred object return result of event.
        :param data: Received data.
        :param address: Address of transmitter.
        """
        self.addr = address
        self.s_example(data).addCallback(self.s_response)

    @defer.inlineCallbacks
    def s_example(self, mess):
        """
        Result of searching in file or writing in it.
        :param mess: Incoming message
        """
        mess = eval(mess)
        doc = yield self.s_srch(mess)
        if doc:
            returnValue(doc)

    def s_srch(self, mess):
        """
        Writing or reading from file.
        :param mess: Data for searching in file.
        :return: String.
        """
        if mess[0]:
            with open('tmp') as f:
                for data in f.readlines()[::-1]:
                    if data.startswith(mess[1]):
                        return data.replace('\n', '')
        elif not mess[0]:
            with open('tmp', 'a') as f:
                f.write(str(mess[1]) + str(mess[2])+'\n')
                return 'Done'
        return 'Empty'

    def s_response(self, docs):
        """
        Send data to transmitter.
        :param docs: Incoming result of searching or writing
        """
        self.transport.write(docs, self.addr)


if __name__ == '__main__':
    protocol = Twist()
    logging.info('Start')
    reactor.listenUDP(4444, protocol)
    reactor.run()
