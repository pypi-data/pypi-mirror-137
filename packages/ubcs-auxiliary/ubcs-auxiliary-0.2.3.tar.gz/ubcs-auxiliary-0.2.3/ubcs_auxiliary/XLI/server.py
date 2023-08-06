#!/bin/env python
"""
The server LL code for the hierarchical level instrumentation

author: Valentyn Stadnytskyi NIH\LCP
data: Sept 2018 - Nov 20 2018

0.0.2 - code under development
0.0.3 - changed init_server function. It was altering the way how logging was working in higher up modules
"""
__version__ = "0.0.3"
__date__ = "November 20, 2018"



import traceback
from pdb import pm

from numpy import nan, mean, std, nanstd, \
     asfarray, asarray, hstack, array, concatenate, \
     delete, round, vstack, hstack, zeros, transpose, \
     split, unique, nonzero, take, savetxt, min, max
from time import time, sleep, clock
import sys
import os.path

from time import gmtime, strftime, time
from logging import debug,info,warning,error


from ubcs_auxiliary.threading import new_thread

from struct import pack, unpack
from timeit import Timer, timeit

from datetime import datetime

import msgpack
import msgpack_numpy as m
import socket

import platform
server_name = platform.node()

class Server_LL(object):

    def __init__(self, name = '', ports = range(2030,2051)):
        """
        to initialize an instance and create main variables
        """
        if len(name) == 0:
            self.name = 'test_communication_LL'
        else:
            self.name = name
        self.running = False
        self.network_speed = 12**6 # bytes per second
        self.push_subscribe_lst = []
        self.last_call_lst = []

    def init_server(self, name = '', ports = range(2030,2051)):
        '''
        Proper sequence of socket server initialization
        '''
        if len(name) == 0:
            self.name = 'test_communication_LL'
        else:
            self.name = name
        self.sock = self.init_socket(ports = ports)
        self._set_commands()
        if self.sock is not None:
            flag = True
        else:
            flag = False
        if flag:
            self._start()
        info('server init.server')

    def stop(self):
        self.running = False
        self.sock.close()

    def init_socket(self,ports = range(2030,2051)):
        '''
        initializes socket for listening, creates sock and bind to '' with a port somewhere between 2030 and 2050
        '''
        import socket
        for port in ports:
            flag = False
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('', port))
                flag = True
            except:
                pass
            if flag:
                self.port = port
                try:
                    self.ip_address = socket.gethostbyname(socket.gethostname())
                except:
                    self.ip_address = '127.0.0.1'
                sock.listen(100)
                break
            else:
                sock = None
                self.port = None
        info('server init.socket: port %r' %(port))
        return sock

    def _set_commands(self):
        """
        Set type definition, the dictionary of command excepted by the server
        Standard supported commands:
        - "help"
        - "init"
        - "close"
        - "abort"
        - "snapshot"
        - "subscribe"
        - "task"
        - "controlls"
        - "indicators"
        - "push_updates"
        """
        self.commands = {}
        self.commands[b'help'] = None
        self.commands[b'init'] = None
        self.commands[b'close'] = None
        self.commands[b'abort'] = None
        self.commands[b'snapshot'] = None
        self.commands[b'subscribe'] = None
        self.commands[b'task'] = None
        self.commands[b'controls'] = None
        self.commands[b'indicators'] = None
        self.commands[b'push_updates'] = None


    def set_tasks(self):
        self.tasks = {}
        self.tasks[b'push updates'] = 'push updates'


    def _get_commands(self):
        """
        returns the dictionary with all supported commands
        """
        return self.commands

    def _start(self):
        '''
        creates a separete thread for server_thread function
        '''
        new_thread(self._run)

    def _run(self):
        """
        runs the function _run_once in a while True loop
        """
        self.running = True
        while self.running:
            self._run_once()
        self.running = False

    def _run_once(self):
        """
        creates a listening socket.
        """

        client, addr = self.sock.accept()
        info('Client has connected: %r,%r' %(client,addr))

        try:
            msg_in = self._receive(client)
            debug('msg in %r' % msg_in)
        except:
            msg_in = {b'command':b'unknown',b'message':b'unknown'}
            error('%r, with input message%r' %(traceback.format_exc(),msg_in))
        msg_out = self._receive_handler(msg_in,client)
        self._send(client,msg_out)

        try:
            message = list(msg_in[b'message'].keys())
        except:
            message = msg_in[b'message']
        self._log_last_call(client, addr, command = msg_in[b'command'], message = message)
        info('Client has been served: %r,%r' %(client,addr))


    def _transmit_handler(self,command = '', message = ''):
        from time import time
        res_dic  = {}
        res_dic[b'command'] = command
        res_dic[b'time'] = time()
        res_dic[b'message'] = message
        return res_dic

    def _receive_handler(self,msg_in,client):
        """
        the incoming msg_in has N mandatory fields:  command, message and time
        """
        from time import time
        res_dic = {}
        #the input msg has to be a dictionary. If not, ignore. FIXIT. I don't know how to do it in Python3
        debug('_receive_handler: command received: %r' % msg_in)
        err = ''
        try:
            keys = msg_in.keys()
            command = msg_in[b'command']
            message_in =  msg_in[b'message']
            debug('_receive_handler: message_in %r, command %r' %(message_in,command))
            res_dic[b'command'] = command
            flag = True
            if command in list(self.commands.keys()):
                if self.commands[command] != None:
                    res_dic = self.commands[command](msg_in = message_in,client = client)
                else:
                    res_dic[b'message'] = None
                    err += 'the %r function is not linked' %(command)
            else:
                flag = False
                err += 'the command %r is not supported by the server.' % command
        except:
            error(traceback.format_exc())
            err += traceback.format_exc()
            res_dic[b'command'] = 'unknown'
            res_dic[b'message'] = 'The quote of the day: FIXIT I hope you enjoyed it.'
            res_dic[b'flag'] = False
            res_dic[b'error'] = err
        res_dic[b'time'] = time()
        res_dic[b'error'] = err
        debug('_receive_handler: res_dic %r' % res_dic)
        return res_dic


    def _receive(self,client):
        """
        descritpion:
        client sends 20 bytes with a number of expected package size.
        20 bytes will encode a number up to 10**20 bytes.
        This will be enough for any possible size of the transfer

        input:
        client - socket client object

        output:
        unpacked data
        """
        import msgpack
        import msgpack_numpy as msg_m
        a = client.recv(20)
        length = int(a)
        if length != 0:
            msg_in = ''.encode()
            while len(msg_in) < length:
                msg_in += client.recv(length - len(msg_in))
                if len(msg_in) < length:
                    sleep(0.01)
        else:
            msg_in = ''
        response = msgpack.unpackb(msg_in, object_hook=msg_m.decode)
        return response

    def _send(self,client,msg_out):
        """
        descrition:
        uses msgpack to serialize data and sends it to the client
        """
        debug('command send %r' % msg_out)
        msg = msgpack.packb(msg_out, default=m.encode)
        length = str(len(msg))
        if len(length)!=20:
            length = '0'*(20-len(length)) + length
        try:
            client.sendall(length.encode())
            client.sendall(msg)
            flag = True
        except:
            error(traceback.format_exc())
            flag = False
        return flag

    def _connect(self,ip_address,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.settimeout(1)
            server.connect((ip_address , port))
            server.settimeout(None)
            debug("Connection success!")
        except:
            error('%r' %(traceback.format_exc()))
            server = None
        return server

    def _transmit(self,command = '', message = '' ,ip_address = '127.0.0.1',port = 2030):
        if isinstance(message,dict):
            pass
            #message[b'ip_address'] = ip_address
            #message[b'port'] = port
        else:
            message = {}
            #message[b'ip_address'] = ip_address
            #message[b'port'] = port
        msg_out = self._transmit_handler(command = command, message = message)
        debug("_transmit msg out (%r)" % msg_out)
        client = self._connect(ip_address = ip_address,port = port)
        debug("connected to the client (%r)" % client)
        if client is not None:
            flag = self._send(client,msg_out)
            self.response_arg = self._receive(client)
            self._server_close(client)
        else:
            self.response_arg = None
        return self.response_arg

    def _server_close(self,server):
        server.close()
        return server

    def _log_last_call(self,client = None, addr = None, command = None, message = None):
        from time import time
        self.last_call_lst = [{b'time':time(),b'ip_address':addr[0], b'command':command,b'message':message}]
        #if len(self.last_call_lst) > 10:
            #self.last_call_lst.pop(0)

#***************************************************
#*** wrappers for basic response functions *********
#***************************************************

    def help(self,msg_in  =None, client = None):
        msg = {}
        msg[b'server name']= self.name
        msg[b'server port']= self.port
        msg[b'server ip address']= socket.gethostbyname(socket.gethostname())
        msg[b'server version']= __version__
        msg[b'commands'] = list(self.commands.keys())
        #msg[b'tasks'] = self.dev_get_tasks
        try:
            try:
                getattr(device.controls,'running')
            except:
                err = 'device offline'
            msg[b'device help'] = self.commands[b'help']()
        except:
            error(traceback.format_exc())
            msg[b'controls'] = 'device offline'
            msg[b'indicators'] = 'device offline'
        return msg

    def subscribe(self,client = None,msg_in = {}):
        from time import time
        new_client_dic = {}
        msg = {}
        err = ''
        new_client_dic[b'port'] = msg_in[b'port']
        new_client_dic[b'ip_address'] = client.getpeername()[0]
        new_client_dic[b'controls'] = msg_in[b'controls']
        new_client_dic[b'indicators'] = msg_in[b'indicators']
        try:
            self.push_subscribe_lst.pop(self.push_subscribe_lst.index(new_client_dic))
        except:
            info(traceback.format_exc())
        self.push_subscribe_lst.append(new_client_dic)
        msg[b'flag'] = True
        msg[b'error'] = err
        return msg

    def push_subscribed_updates(self, controls = [], indicators = [], subscriber = -1):
        """
        pushes updates to subscribed clients stored in self.push_subscriber_lst
        """
        if len(controls) == 0:
            debug('server_LL: the list of controls names ie empty. Nothing to push. Indicators: %r' % indicators)
        if len(indicators) == 0:
            debug('server_LL: the list of indicators names ie empty. Nothing to push. Controls: %r' % controls)
        try:
            a = self.push_subscribe_lst[subscriber]
        except:
            debug("subscriber %r in server.push_subscribed_updates doesn't exist" %(subscriber))
            subscriber = -1

        if subscriber == -1:
            push_subscriber_lst = self.push_subscribe_lst
        else:
            push_subscriber_lst = [self.push_subscribe_lst[subscriber]]

        #Stepping through all subscribers in push_subscriber_lst
        for client_dic in push_subscriber_lst:
            indicators_dic = {}
            controls_dic = {}
            msg_dic = {}
            debug("if indicators in %r" % client_dic.keys())

            #checks if client subscribed to indicators
            if b'indicators' in list(client_dic.keys()) and len(indicators) !=0:
                if indicators == [b'all']:
                    for item in client_dic[b'indicators']:
                        indicators_dic[item] = None
                else:
                    for item in indicators:
                        if item in client_dic[b'indicators']:
                            indicators_dic[item] = None
                debug("push_subscribed_updates indicators_dic = %r" % indicators_dic)
                msg_dic[b'indicators']= self.commands[b'indicators'](msg_in = indicators_dic)
            else:
                msg_dic[b'indicators'] = ''


            if b'controls' in list(client_dic.keys()) and len(controls) !=0:
                debug("push_subscribed_updatescontrols = %r" % controls)
                if controls == [b'all']:
                    for item in client_dic[b'controls']:
                        controls_dic[item] = None
                else:
                    for item in controls:
                        if item in client_dic[b'controls']:
                            controls_dic[item] = None
                debug("push_subscribed_updates controls_dic = %r" % controls_dic)
                msg_dic[b'controls'] = self.commands[b'controls'](controls_dic)
            else:
                msg_dic[b'controls'] = ''

            debug('client_dic %r' % client_dic)
            debug('msg = '+str(msg_dic))
            response = 0
            try:
                if len(indicators_dic) != 0:
                    response = self._transmit(command = 'indicators',
                                   message = msg_dic[b'indicators'] ,
                                   ip_address = client_dic[b'ip_address'],
                                   port = client_dic[b'port'])

                if len(controls_dic) != 0:
                    response = self._transmit(command = 'controls',
                                   message = msg_dic[b'controls'] ,
                                   ip_address = client_dic[b'ip_address'],
                                   port = client_dic[b'port'])
            except:
                response = None
                warning(traceback.format_exc())
            if response == None:
                index = self.push_subscribe_lst.index(client_dic)
                self.push_subscribe_lst.pop(index)
                info('The subscribed client\server is not avaiable.')




server = Server_LL()


if __name__ == "__main__": #for testing
    from tempfile import gettempdir
    import logging
    logging.basicConfig(#filename=gettempdir()+'/communication_LL.log',
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
    server = Server_LL(name = 'client')
    self = server
    server.init_server()

    info('Server: is running at %r,%r and port %r' %(server.sock.getsockname(),
                                                      socket.gethostbyname(socket.gethostname()),
                                                      server.port))
