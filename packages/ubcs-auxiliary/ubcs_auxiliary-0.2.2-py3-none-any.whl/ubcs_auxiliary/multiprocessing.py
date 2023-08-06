def new_child_process(function,  *args, **kwargs):
    """
    launches the input 'function' in a separate thread with daemon == True.

    Explanation: Some threads do background tasks, like sending keepalive packets, or performing periodic garbage collection, or whatever. These are only useful when the main program is running, and it's okay to kill them off once the other, non-daemon, threads have exited.

    Without daemon threads, you'd have to keep track of them, and tell them to exit, before your program can completely quit. By setting them as daemon threads, you can let them run and forget about them, and when your program quits, any daemon threads are killed automatically.
    @Chris Jester-Young https://stackoverflow.com/a/190017/8436767

    Parameters
    ----------
    function:
        function object
    *args:
        iterable of arguments
    **kwargs:
        dictionary of keywords

    Returns
    -------
    process:
        process object

    Examples
    --------
    the example of usage

    >>> def func(*args,**kwargs):
            print('keywords',kwargs)
            print('args',args)
            from time import time,sleep
            t1 = time()
            sleep(args[0])
            t2 = time()
            print('this thread slept for {} seconds'.format(t2-t1))
            print('input parameters: args = {}, kwargs = {!r}'.format(args[0],kwargs['keyword']))
    >>> new_child_process(func, 1, keyword = 'this is key 1 value')
    this thread slept for 1.002244234085083 seconds
    input parameters: args = 1, kwargs = 'keywords argument'
    """
    from multiprocessing import Process
    p = Process(target=function, args=args, kwargs = kwargs)
    p.daemon = True
    p.start()
    return p

class ParallelProcessing():
    def __init__(self, function, iter, *args, **kwargs):
        """
        This is a specialized wrapper around multiprocessing.Process object. It
        launches multiple separate processes with the same input 'function' but different argument that comes from an iterable object like tuple or list.

        Parameters
        ----------
        function :: function
            function object
        args :: list or tuple
            iterable of arguments
        kwargs :: dictionary
            keyword arguments that will be passed to the function

        Returns
        -------
        jobs :: list
            list of jobs

        Examples
        --------
        >>> mp = ParallelProcessing(function, (1,2,3))
        """
        from multiprocessing import Process
        print(args,kwargs)
        self.jobs = []
        for arg in args:
            p = Process(target=function,args=(arg,), **kwargs)
            p.daemon = True
            p.start()
            self.jobs.append(p)

class MultiProcessing():
    def __init__(self, function, args, **kwargs):
        """
        This is a specialized wrapper around multiprocessing.Process object. It
        launches multiple separate processes with the same input 'function' but different argument that comes from an iterable object like tuple or list.

        Parameters
        ----------
        function :: function
            function object
        args :: list or tuple
            iterable of arguments
        kwargs :: dictionary
            keyword arguments that will be passed to the function

        Returns
        -------
        jobs :: list
            list of jobs

        Examples
        --------
        >>> mp = ParallelProcessing(function, (1,2,3))
        """
        from multiprocessing import Process
        print(args,kwargs)
        self.jobs = []
        for arg in args:
            p = Process(target=function,args=(arg,), **kwargs)
            p.start()
            self.jobs.append(p)
        import warnings
        warnings.warn("MultuProcessing class will be deprecated in future versions. The new name is ParallelProcessing", DeprecationWarning)

def function(N, **kwargs):
    """
    an example function for test purposes. It sleeps for N seconds. Prints statements when sleep starts and finishes.
    """
    from time import time, sleep

    print_text_kwarg(**kwargs)
    print_dict_kwarg(**kwargs)
    print_var_kwarg(**kwargs)

    print('Starting Process')
    t1 = time()
    print('[{} s] Start sleeping for {} seconds'.format(round(time()-t1,4),N))
    print('[{} s] Sleeping... '.format(round(time()-t1,4)))
    sleep(N)
    print('[{} s] Done sleeping for {} seconds'.format(round(time()-t1,4),N))

def print_text_kwarg(**kwargs):
    print(f"kwarg text = {kwargs['text']}")
def print_dict_kwarg(**kwargs):
    print(f"kwarg dict = {kwargs['dict']}")
def print_var_kwarg(**kwargs):
    print(f"kwarg var = {kwargs['var']}")

def test():
    """
    simple test showing how to use
    """
    kwargs = {'text': 'my new text', 'var' : 15.64, 'dict' : {'key':'my new value'}}
    mp = MultiProcessing(function, args = (1,2,3), kwargs = kwargs)

def test2():
    """
    simple test showing how to use
    """
    kwargs = {'text': 'my new text', 'var' : 15.64, 'dict' : {'key':'my new value'}}
    mp = ParallelProcessing(function, args = (1,2,3), kwargs = kwargs)

def test3(root, t = 120):
    from time import time, ctime, sleep
    import os
    filename = os.path.join(root,str(time())+'.txt')
    print(root,t)
    t_start = time()
    while time()-t_start <=t:
        with open(filename,'a') as f:
            f.write(str(ctime(time()))+'\n')
            sleep(1)
    print('the process is done')
