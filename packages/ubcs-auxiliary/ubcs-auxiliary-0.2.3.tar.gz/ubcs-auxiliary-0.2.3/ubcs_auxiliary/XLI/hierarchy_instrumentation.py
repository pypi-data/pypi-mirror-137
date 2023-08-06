"""
XLevel delocalized instrumentation class
author: Valentyn Stadnytskyi
Created: November 2017
Last modified: March 7 2019
"""

__version__ = '0.0.2'

import traceback
import psutil, os
import platform #https://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
p = psutil.Process(os.getpid()) #source: https://psutil.readthedocs.io/en/release-2.2.1/


from numpy import nan, mean, std, nanstd, asfarray, asarray, hstack, array, concatenate, delete, round, vstack, hstack, zeros, transpose, split, unique, nonzero, take, savetxt, min, max
from serial import Serial
from time import time, sleep
import sys
import os.path
import struct
from pdb import pm
from time import gmtime, strftime, time
from logging import debug,info,warning,error


from struct import pack, unpack
from timeit import Timer, timeit

from threading import Thread, Event, Timer, Condition
from datetime import datetime

class GUITemlpate():
    def __init__(self):
        pass

    def initGUI(self):
        pass

class IndicatorsTemplate():

    def __init__(self, object):
        self.object = object
        self.list = []

    def keys(self):
        if len(self.list) == 0:
            self.list = list(self.get().keys())
        return self.list

    def get(self, value = None):
        """
        returns a dictionary with all indicators. Every entry needs to
        be added manually. This helps to orginize what is avaiable to the outsie
        requestor.
        """
        dic = {}
        dic[b'running'] = self.running

        return dic



    def get_running(self):
        """
        default get_running function in the intrumentation library
        """
        raise NotImplementedError
        #return response
    def set_running(self,value):
        """
        default set_running function in the intrumentation library
        """
        raise NotImplementedError
    running = property(get_running,set_running)

class ControlsTemplate():
    def __init__(self, object):
        self.list = []
        self.object = object

    def keys(self):
        if len(self.list) == 0:
            self.list = list(self.get().keys())
        return self.list


    def get(self):
        dic = {}
        dic[b'variable'] = 0
        return dic

    def set(self,new_controls = [{b'temp':False}]):
        for key in list(new_controls.keys()):
            setattr(self,key.decode("utf-8"),new_controls[key])
        response = self.get()
        return response

    def get_variable(self):
        try:
            response = getattr(self.object,'variable')
        except:
            response = None #device.controls.running
            warning(traceback.format_exc())
        return response
    def set_variable(self,value):
        """
        indicators cannot be set from outside. This method is used to set
        an indicator from other instances within this proccess.
        """
        try:
            setattr(self.object,'variable',value)
        except:
            error(traceback.format_exc())
    variable = property(get_variable,set_variable)

    def get_task_queue(self):
        """
        """
        raise NotImplementedError

    def set_task_queue(self,value):
        """
        """
        raise NotImplementedError
    variable = property(get_variable,set_variable)




class XLevelTemplate():

    #inds = IndicatorsTemplate(self)
    #ctrls = ControlsTemplate(self)
    """circular buffers dictionary contains information about all circular buffers and their type (Server, Client or Queue)"""
    circular_buffers = {}

    def __init__(self):
        #Thread.__init__(self)
        self.running = False
        #self.daemon = False # OK for main thread to exit even if instance is still running
        self.description = ''

    def first_time_setup(self):
        """aborts current operation
        """
        raise NotImplementedError


    def init(self, msg_in = None, client = None):
        """
        does proper start of the XLevel code and can be called remoutely
        """
        raise NotImplementedError
        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response

    def abort(self,msg_in = None, client = None):
        """aborts current operation
        """
        raise NotImplementedError
        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response

    def close(self,msg_in = None, client = None):
        """aborts and completely stops the XLevel code
        """
        raise NotImplementedError

        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response



    def help(self,msg_in = None, client = None):
        """
        returns help information about this XLevel program

        ####
        EXAMPLE:
        response = {}
        response[b'name'] = self.name
        response[b'controls'] = self.ctrls.get()
        response[b'indicators'] = self.inds.get()
        return response
        """
        raise NotImplementedError

        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response

    def snapshot(self,msg_in = None, client = None):
        """
        returns snapshot of selected or all controls and indicators.
        see example below

        EXAMPLE:
        response = {}
        response[b'name'] = self.name
        response[b'controls'] = self.ctrls.get()
        response[b'indicators'] = self.inds.get()
        return response
        """
        raise NotImplementedError

        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response



    def controls(self,msg_in = {b'all':None}, client = None):
        """
        return current control(controls) according to the input dictionary.
        example:
        the command->
        controls(msg = {b'controls':{'button1':None,'button2':None,'scanrate':2.0}})
        will set scanrate to 2.0 and return current setting for button1, button2 and scanrate
        """
        debug('icarusSL controls command received: %r' % msg_in)
        response = {}
        msg_out = {}
        msg_out[b'message'] = {}
        err = ''
        flag = True
        if isinstance(msg_in,dict):
            if b'all' in list(msg_in.keys()):
                    response = self.ctrls.get()
                    ctrls_keys = self.ctrls.keys()
            else:
                ctrls_keys = self.ctrls.keys()
                for key in msg_in:
                    if msg_in[key] is None:
                        if key in ctrls_keys:
                            response[key] = getattr(self.ctrls,key.decode("utf-8"))
                        else:
                            response[key] = None
                            err = "control doesn't exist"
                    else:
                        if key in ctrls_keys:
                            setattr(self.ctrls,key.decode("utf-8"),msg_in[key])
                            response[key] = getattr(self.ctrls,key.decode("utf-8")) #msg_in[key]
                        else:
                            response[key] = None
                            err = "control doesn't exist"

        msg_out[b'flag'] = flag
        msg_out[b'message'][b'controls'] = response
        msg_out[b'error'] = err
        return msg_out

    def indicators(self, msg_in = {b'all':None}, client = None):
        """
        this function takes 7us to execute probably because of hashtable,etc.
        If I call the function directly, I can execute it in 1 us
        """
        debug('icarusSL indicators command received: %r' % msg_in)
        response = {}
        msg_out = {}
        msg_out[b'message'] = {}
        err = ''
        flag = True
        if isinstance(msg_in,dict):
            if b'all' in list(msg_in.keys()):
                    response = self.inds.get()
                    inds_keys = self.inds.keys()
            else:
                inds_keys = self.inds.keys()
                for key in msg_in:
                    if msg_in[key] is None:

                        if key in inds_keys:
                            response[key] = getattr(self.inds,key.decode("utf-8"))
                        else:
                            response[key] = None
                            err = "indicator doesn't exist"
                    else:
                        if key in inds_keys:
                            setattr(self.inds,key.decode("utf-8"),msg_in[key])
                            response[key] = getattr(self.inds,key.decode("utf-8"))
                        else:
                            response[key] = None
                            err = 'error'
        msg_out[b'flag'] = flag
        msg_out[b'message'][b'indicators'] = response
        msg_out[b'error'] = err
        return msg_out

    def notify_subscribers(self, msg_in = None, client = None):

        raise NotImplementedError

    def schedule(self, task_list = []):
        try:
            self.controls.set({b'task_queue':task_list})
            flag = True
        except:
            error(traceback.format_exc())
            flag = False

        response = {}
        response[b'flag'] = flag
        response[b'message'] = message
        response[b'error'] = err
        return response
###
    ##########################################
    ### TASK SECTION: schedule, execute and abort
    #######################################
    """
    This section is dedicated to functions that take care of
    the queue task consept and help to execute it.
    """
    def schedule_task_queue(self, task_list = []):
        try:
            self.controls.set({b'task_queue':task_list})
            response = True
        except:
            error(traceback.format_exc())
            response = False
        return response

    def abort_task_queue(self):
        try:
            self.controls.set({b'task_queue':[]})
            response = True
        except:
            error(traceback.format_exc())
            response = False
        return response

    def execute_task_queue(self):
        if len(self.controls.task_queue) > 0:
            if self.controls.task_queue[0][0] - time() <=0:
                try:
                    info('executing: %r, with flag %r' %
                         (self.controls.task_queue[0],
                          self.controls.task_queue[0][1] == b'change_offset'))
                    if self.controls.task_queue[0][1] == b'change_offset' or self.controls.task_queue[0][1] == 'change_offset':

                        self.change_offset(self.controls.task_queue[0][2][b'offset'])
                    self.controls.task_queue.pop(0)
                except:
                    pass#error(traceback.format_exc())
                flag = True
            else:
                flag = False
        else:
            flag = False
        return flag

    #########
    ### OTHER TASKS GO HERE. The XLevel can support multiple additional tasks
    ### which are more complicated than just return indicators or controls
    ########
    #def start(self): This is not needed for the class Thread
    #    """"""
    #    raise NotImplementedError

    def stop(self):
        """"""
        raise NotImplementedError

    def run_once(self):
        """"""
        raise NotImplementedError

    def run(self):
        """"""
        self.running = True
        while self.running:
            self.run_once()
            sleep(1)
        raise NotImplementedError


    def get_circular_buffer(self, msg_in = None, client = None):
        """
        returns data from server circular buffer. Input, name of the circular buffer and global pointer.
        msg_in has to be a dictionary with circular buffer name
        the global_pointer sppecifies
        msg_in = {b'buffer_name':b'name',b'g_pointer':999}
        """
        msg_out = {b'message':{}}
        flag = True
        err = ''

        in_buffer_name = msg_in[b'buffer_name']
        in_g_pointer = msg_in[b'g_pointer']
        if in_buffer_name in self.circular_buffers.keys():
            g_pointer = self.circular_buffers[in_buffer_name].g_pointer
            pointer = self.circular_buffers[in_buffer_name].pointer
            size = self.circular_buffers[in_buffer_name].size
            if in_g_pointer > g_pointer:
                data = self.circular_buffers[in_buffer_name].get_all()
            elif in_g_pointer < g_pointer:
                if g_pointer - in_g_pointer > size[1]:
                    data = self.circular_buffers[in_buffer_name].get_all()
                else:
                    N = g_pointer - in_g_pointer
                    data = self.circular_buffers[in_buffer_name].get_N(N, M = pointer)
            else:
                data = None

            self.circular_buffers[in_buffer_name]

        msg_out[b'flag'] = flag
        msg_out[b'message'][b'data'] = data
        msg_out[b'message'][b'g_pointer'] = g_pointer
        msg_out[b'message'][b'pointer'] = pointer
        msg_out[b'error'] = err
        return msg_out

    def retrieve_values(self, msg_in = None , N = 2, order = 2, test_flag = None, client = None):
        """
        msg_in = {b'buffer_name':b'name',b'time_vector' = asarray([ 1,  1,  1,  1,  1,  1,  1])}
        N - number of points to concider when obtain estimated value
        """
        from numpy import argmin, argwhere, loadtxt, nanmax,\
             nanmin, nan, nanargmin, nanargmax

        from XLI.auxiliary import sort_vector, expand_vector, get_estimate


        msg_out = {b'message':{}}
        flag = True
        err = ''
        out_array = None

        if isinstance(msg_in,dict):
            in_buffer_name = msg_in[b'buffer_name']
            in_vector = sort_vector(msg_in[b'time_vector'])
            if in_buffer_name in self.circular_buffers.keys():
                ndim = self.circular_buffers[in_buffer_name].size[0]
                out_array = expand_vector(in_vector, ndim = ndim)
                for i in range(len(in_vector)):
                    for j in range(1,ndim):
                        x = self.circular_buffers[in_buffer_name].get_all()[0,:]
                        y = self.circular_buffers[in_buffer_name].get_all()[j,:]
                        x_est = in_vector[i]
                        if x_est > nanmax(x):
                            y_est = nan
                            err += 'requested value(%r) outside of the buffer boundaries. value > nanmax (%r)' % (x_est,nanmax(x))
                        elif x_est < nanmin(x):
                            y_est = nan
                            err += 'requested value(%r) outside of the buffer boundaries. value < nanmin (%r)' % (x_est,nanmin(x))
                        else:
                            idx = nanargmin((x - x_est)**2)
                            debug('idx = %r' %idx)
                            if idx >= len(x)-2:
                                N_after = 0
                                N_before = N
                            elif idx <= 1:
                                N_after = N+1
                                N_before = 0
                            else:
                                N_after = N+1
                                N_before = N
                            debug('N_after %r, N_before %r' %(N_after,N_before))

                            y_est = get_estimate(x[idx-N_before:idx+N_after],y[idx-N_before:idx+N_after],x_est, order = order)

                        out_array[j,i] = y_est

            else:
                err = "buffer doesn't exist"
                out_vector = msg_in[b'time_vector']
        msg_out[b'flag'] = flag
        msg_out[b'message'][b'out_array'] = out_array
        msg_out[b'error'] = err
        return msg_out
########################################
###  Threading Section   ###
####################################

###BINDING OF A SERVER MODULE WITH XLevel EXAMPLE

##from server_LL import server
##server.init_server(name = 'icarus-server')
##server.commands[b'init'] = icarus_SL.init
###server.commands[b'help'] = device.help
###server.commands[b'snapshot'] = device.snapshot
###server.commands[b'close'] = device.close
##server.commands[b'controls'] = icarus_SL.controls
##server.commands[b'indicators'] = icarus_SL.indicators
###server.commands[b'retrieve_values'] = device.retrieve_values
##server.commands[b'subscribe'] = server.subscribe
###server.commands[b'buffers_update'] = device.buffers_update
###server.commands[b'dump_buffers'] = icarus_SL.subscribe



if __name__ == "__main__": #for testing
    from tempfile import gettempdir
    import logging
    #logging.basicConfig(#filename=gettempdir()+'/icarus_SL.log',
     #                   level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
