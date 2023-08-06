def new_thread(function, *args, **kwargs):
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
            daemon:
                flag, if the thread is daemon(True) or not(False).


    Returns
    -------
    thread:
        thread object

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
    >>> new_thread(func, 1, keyword = 'this is key 1 value')
    this thread slept for 1.002244234085083 seconds
    input parameters: args = 1, kwargs = 'keywords argument'

    """
    from threading import Thread
    thread = Thread(target=function, args = args, kwargs = kwargs)
    try:
        daemon = kwargs['daemon']
    except:
        daemon = True
    thread.daemon = daemon
    thread.start()
    return thread

def start_new_safe_thread(function, daemon = True, *args ,  **kwargs):
    """
    alias for new_thread for back compatibility
    """
    import warnings
    warnings.warn(
            "start_new_safe_thread will be deprecated in version 0.0.7, use new_thread instead",
             PendingDeprecationWarning
        )
    return new_thread(function, args , kwargs)
