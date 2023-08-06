#!/bin/env python
"""
The server LL code for the hierarchical level instrumentation

author: Valentyn Stadnytskyi NIH\LCP
data: Sept 2018 - Nov 2 2018

The server has the basic set of functions:
0) init
1) close
2) abort
3) subscribe (on/off)
4) snapshot
5) task
6)

0.0.2 - code under development
"""
__version__ = "0.0.3"
__date__ = "November 2, 2018"


from time import time, sleep, clock
import sys
import os.path
import struct
from pdb import pm
from time import gmtime, strftime, time
from logging import debug,info,warning,error
import traceback
if sys.version_info[0] ==3:
    from _thread import start_new_thread
else:
    from thread import start_new_thread

from struct import pack, unpack
from timeit import Timer, timeit

from datetime import datetime

import msgpack
import msgpack_numpy as m
import socket

import platform
server_name = platform.node()
from threading import Thread
class Client_LL(Thread):

    def __init__(self, name = ''):
        """
        to initialize an instance and create main variables
        """
        Thread.__init__(self)
        if len(name) == 0:
            self.name = 'test_communication_LL'
        else:
            self.name = name
        self.running = False
        self.network_speed = 12**6 # bytes per second
        self.push_subscribe_lst = []
        self.last_call_lst = []
        self.connection_timeout = 3.0 #timeout in seconds
        self.device = {}

    def init_server(self):
        '''
        Proper sequence of socket server initialization
        '''
        self._set_commands()
        self.sock = self.init_socket()
        if self.sock is not None:
            self.running = True
        else:
            self.running = False
        if self.running:
            self.start()

    def stop(self):
        self.running = False
        self.sock.close()

    def init_socket(self):
        '''
        initializes socket for listening, creates sock and bind to '' with a port somewhere between 2030 and 2050
        '''
        import socket
        ports = range(2030,2050)
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('', port))
                self.port = port
                sock.listen(100)
                flag = True
            except:
                error(traceback.format_exc())
                flag = False
            if flag:
                break
            else:
                sock = None
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
        self.tasks['push updates'] = 'push updates'


    def _get_commands(self):
        """
        returns the dictionary with all supported commands
        """
        return self.commands

    def _start(self):
        '''
        creates a separete thread for server_thread function
        '''
        start_new_thread(self._run,())

    def _run(self):
        """
        runs the function _run_once in a while True loop
        """
        self.running = True
        while self.running:
            self._run_once()
        self.running = False

    def run(self):
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
        debug('Client has connected: %r,%r' %(client,addr))
        self._log_last_call(client, addr)
        msg_in = self._receive(client)
        try:
            pass
        except:
            msg_in = {b'command':b'unknown',b'message':b'unknown'}
            error('%r, with input message%r' %(traceback.format_exc(),msg_in))
        debug(msg_in)
        msg_out = self._receive_handler(msg_in,client)
        self._send(client,msg_out)

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
        self.last_received_message = msg_in

        try:
            keys = msg_in.keys()
            command = msg_in[b'command']
            message_in =  msg_in[b'message']
            res_dic[b'command'] = command
            flag = True
            if self.commands[command] != None:
                self.commands[command](msg_in = message_in,client = client)
            else:
                flag = False
                err = 'the command %r is not supporte by the server' % command
            if not flag:
                debug('command is not recognized')
                res_dic[b'command'] = 'unknown'
                res_dic[b'message'] = 'The quote of the day: ... . I hope you enjoyed it.'
                res_dic[b'flag'] = flag
                res_dic[b'error'] = err
            else:
                res_dic[b'flag'] = flag
                res_dic[b'error'] = ''
        except:
            error(traceback.format_exc())
            res_dic[b'command'] = 'unknown'
            res_dic[b'message'] = 'The quote of the day: ... . I hope you enjoyed it.'
            res_dic[b'flag'] = True
            res_dic[b'error'] = ''
        res_dic[b'time'] = time()

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
        sleep(0.01)
        if length != 0:
            msg_in = ''.encode()
            while len(msg_in) < length:
                msg_in += client.recv(length - len(msg_in))
                sleep(0.01)
        else:
            msg_in = ''
        return msgpack.unpackb(msg_in, object_hook=msg_m.decode)

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
            server.settimeout(self.connection_timeout)
            server.connect((ip_address , port))
            debug("Connection success!")
        except:
            error('%r' %(traceback.format_exc()))
            server = None
        return server

    def _transmit(self,command = '', message = '' ,ip_address = '0.0.0.0',port = 2030):
##        if isinstance(message,dict):
##            message[b'ip_address'] = ip_address
##            message[b'port'] = port
##        else:
##            message = {}
##            message[b'ip_address'] = ip_address
##            message[b'port'] = port
        msg_out = self._transmit_handler(command = command, message = message)
        #print('msg_out %r' % msg_out)
        server = self._connect(ip_address = ip_address,port = port)
        #print('server %r' % server)
        debug(server)
        if server is not None:
            flag = self._send(server,msg_out)
            #print('flag %r' % flag)

            response_arg = self._receive(server)
            #print('response_arg %r' % response_arg)

            self._client_close(server)
        else:
            response_arg = None
        return response_arg

    def _client_close(self,server):
        server.close()
        return server

    def _log_last_call(self,client,addr):
        from time import time
        self.last_call_lst = [{'time':time(),'ip_address':addr[0]}]
        #if len(self.last_call_lst) > 10:
            #self.last_call_lst.pop(0)

#***************************************************
#*** wrappers for basic response functions *********
#***************************************************

    def help(self):
        msg = {}
        msg[b'client name']= self.name
        msg[b'client port']= self.port
        msg[b'client ip address']= socket.gethostbyname(socket.gethostname())
        msg[b'client version']= __version__
        msg[b'commands'] = self.commands
        #msg['tasks'] = self.dev_get_tasks
        try:
            try:
                getattr(device.controls,'running')
            except:
                err = 'device offline'
            msg[b'device name'] = device.name
            msg[b'device version'] = device.version
            msg[b'controls'] = self.controls()
            msg[b'indicators'] = self.indicators()
        except:
            msg[b'controls'] = 'device offline'
            msg[b'indicators'] = 'device offline'
        return msg



    def identify(self, ip_address = '', port = 0, device = None):
        debug('init command request to  %r %r ' % (ip_address,port))
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
                response = self._transmit(command = b'help',
                             message = '',
                             ip_address = ip_address,
                             port = port)
            except:
                err = traceback.format_exc()
                error(err)
                response = err
        else:
            response = self._transmit(command = b'help',
                             message = '',
                             ip_address = ip_address,
                             port = port)
        return response

    def init(self, device = {b'ip_address':'127.0.0.1',
                             b'port':2040,
                             b'name':b'localhost'}):
        debug('init command request to  %r %r ' % (device[b'ip_address'],device[b'port']))
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
                response = self._transmit(command = b'init',
                             message = '',
                             ip_address = ip_address,
                             port = port)
            except:
                err = traceback.format_exc()
                error(err)
                response = err
        else:
            response = self._transmit(command = b'init',
                             message = '',
                             ip_address = ip_address,
                             port = port)
        return response

    def close(self, ip_address = '127.0.0.1', port = 2030,
              device = None):
        debug('close command request to  %r %r ' % (ip_address,port))
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'close',
                         message = '',
                         ip_address = ip_address,
                         port = port)
        return response

    def cstart(self,ip_address = '127.0.0.1', port = 2030,
              device = None):
        debug('close command received with message = %r' % msg)
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'start',
                     message = '',
                     ip_address = ip_address,
                     port = port)
        return response

    def stop(self,ip_address = '127.0.0.1', port = 2030,
              device = None):
        debug('close command received with message = %r' % msg)
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'stop',
                         message = '',
                         ip_address = ip_address,
                         port = port)
        return response

    def abort(self, ip_address = '', port = 0,
              device = None):
        debug('abort command request to  %r %r ' % (ip_address,port))
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'abort',
                         message = '',
                         ip_address = ip_address,
                         port = port)
        return response

    def snapshot(self, ip_address = '', port = 0, device = None):
        debug('snapshot command request to  %r %r ' % (ip_address,port))
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
                response = self._transmit(command = b'snapshot',
                             message = '',
                             ip_address = ip_address,
                             port = port)
            except:
                err = traceback.format_exc()
                error(err)
                response = err
        else:
            response = self._transmit(command = b'snapshot',
                             message = '',
                             ip_address = ip_address,
                             port = port)
        return response

    def task(self,msg):
        if isinstance(msg,list) and isinstance(msg[0],list):
            device.set_task_queue(msg)
            response = len(server.controls({b'task_queue':None})[b'controls'][b'task_queue'][0])
        else:
            response = 'error'
        return response

    def controls(self,
                   controls = {b'all':None},
                   device = {b'ip_address':'127.0.0.1',
                             b'port':2030,
                             b'name':b'localhost'}):
        """
        return current control(controls) according to the input dictionary.
        example:
        the command->
        controls(msg = {b'controls':{'button1':None,'button2':None,'scanrate':2.0}})
        will set scanrate to 2.0 and return current setting for button1, button2 and scanrate
        """
        debug('controls command received: %r' % controls)
        controls_dic = {}

        for item in list(controls.keys()):
            controls_dic[item] = controls[item]
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'controls',
                         message = controls_dic,
                         ip_address = ip_address,
                         port = port)
        return response
    def get_control(self,control = '',device = {b'ip_address':None,b'port': None}):
        """
        gets the value of the control with the name control from device dictionary
        """
        if control != '':
            response = self.controls(device = device,
                                     controls = {control:None})[b'message'][b'controls'][control]
        else:
            response = None
        return response
    def set_control(self,control = '',
                    device = {b'ip_address':None,b'port' : None},
                    value = None):
        if control != "":
            res_dic = self.controls(device = device, controls = {control:value})
            response = res_dic[b'message'][b'controls'][control]
        else:
            print(res_dic[b'error'])
            error(res_dic[b'error'])
            response = None
        return response

    def indicators(self,
                   indicators = {b'all':None},
                   device = {b'ip_address':'127.0.0.1',
                             b'port':2030,
                             b'name':b'localhost'}):
        """
        this function takes 7us to execute probably because of hashtable,etc.
        If I call the function directly, I can execute it in 1 us
        """
        indicators_dic = {}

        for item in list(indicators.keys()):
            indicators_dic[item] = indicators[item]
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                err = traceback.format_exc()
                error(err)
        response = self._transmit(command = b'indicators',
                         message = indicators_dic,
                         ip_address = ip_address,
                         port = port)

        return response
    def get_indicator(self,indicator = '', device = None):
        response = self.indicators(device = device,
                                   indicators = {indicator:None})[b'message'][b'indicators'][indicator]
        return response


    def subscribe(self,ip_address ='128.231.5.229' ,port = 2030,device = {},indicators = ['all'],controls = ['all']):
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'subscribe',
                         message = {b'port':self.port, b'indicators':indicators, b'controls':controls, b'ip_address':socket.gethostbyname(socket.gethostname())},
                         ip_address = ip_address,
                         port = port)
        return response

    def buffers_update(self, ip_address ='128.231.5.229' ,port = 2030,
                        buffers = {b'all':None},
                        device = None):
        """
        this function takes 7us to execute probably because of hashtable,etc.
        If I call the function directly, I can execute it in 1 us
        """
        buffers_dic = {}
        for item in list(buffers.keys()):
            buffers_dic[item] = buffers[item]
        if isinstance(device,dict):
            try:
                ip_address = device[b'ip_address']
                port = device[b'port']
            except:
                error(err)
        response = self._transmit(command = b'buffers_update',
                         message = buffers_dic,
                         ip_address = ip_address,
                         port = port)

        return response





#######
### Test fuctions
########



client = Client_LL()

#from DAQ_dummy_LL import daq_dummy as device



if __name__ == "__main__": #for testing
    from tempfile import gettempdir
    import logging
    logging.basicConfig(filename=gettempdir()+'/XLI_client_LL.log',
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
    self = client
    client.init_server()
    #server._run_once()
    device = {}

    print("device['ii-50-DL'] = {b'ip_address':'172.17.200.36',b'port':2030}")
    print("device['ii-50-SL'] = {b'ip_address':'172.17.200.36',b'port':2031}")
    print("device['ii-50-AL'] = {b'ip_address':'172.17.200.36',b'port':2032}")
    print("device['icarus-0'] = {b'ip_address':'128.231.5.84',b'port':2030}")
    print("device['icarus-0'] = {b'ip_address':'128.231.5.84',b'port':2030}")
    print("device['icarus-0'] = {b'ip_address':'128.231.5.84',b'port':2030}")


    print('Client: is running at %r,%r'
          %(client.sock.getsockname(),socket.gethostbyname(socket.gethostname())))
    print("client._transmit(command = 'init', message = '', ip_address = '%s', port = %r)"
          % ('127.0.0.1',2035))
    print("client.indicators(device = device['icarus-0'], indicators = {b'running':None})")
    print("client.subscribe(ip_address = '127.0.0.1', port = 2035, device  = None)")
    print("data = client._transmit(command = b'read_queue', message = {b'number':70000},ip_address = '127.0.0.1', port = 2030)[b'message']")
