from ubcs_auxiliary.multithreading import new_thread

def test_start_new_thread():
    print('1')
    def func(*args,**kwargs):
        global sum_value
        global kwargs_list
        from numpy import sum
        sum_value = sum(args)
        kwargs_list = list(kwargs.keys())

    from time import sleep
    global sum_value
    global kwargs_list
    sum_value = None
    kwargs_list = None
    thread = new_thread(func,1,2,3,4,5,6 , keyword1 = '', keyword2 = 5)
    while kwargs_list is None:
        sleep(0.01)
    assert sum_value == 21
    assert kwargs_list == ['keyword1','keyword2']
print('2')
def test_start_new_thread2():
    from time import sleep
    global sum_value
    global kwargs_list
    def func(*args,**kwargs):
        global sum_value
        global kwargs_list
        from numpy import sum
        sum_value = sum(args)
        kwargs_list = list(kwargs.keys())
    sum_value = None
    kwargs_list = None
    new_thread(func,-1,-2,-3,-4,-5,-6, keyword12 = '', keyword22 = 5)
    while kwargs_list is None:
        sleep(0.01)
    assert sum_value == -21
    assert kwargs_list == ['keyword12','keyword22']
print('3')
def test_start_new_thread3():
    from time import sleep
    global value
    value = 0
    def func():
        global value
        value = 5
    new_thread(func)

    sleep(0.01)
    assert value == 5
