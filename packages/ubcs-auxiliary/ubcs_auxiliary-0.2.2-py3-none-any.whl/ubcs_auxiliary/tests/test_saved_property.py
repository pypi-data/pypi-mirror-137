
from ..saved_property import DataBase, SavedProperty

def test_tmpdir(tmpdir):
    print('temp directory is ',tmpdir)

def test_create_a_b(tmpdir):
    """
    Creates a class with default values.
    changes them and destroy itself.
    Create a different instance with the same class and confirm that values were uploaded correctly.
    """
    from random import random
    class A():
        db = DataBase(root = tmpdir, name = 'simpledb')
        a = SavedProperty(db,'a',0.0).init()
        b = SavedProperty(db,'b',0.0).init()
        c = SavedProperty(db,'c',0.0).init()
        d = SavedProperty(db,'d',0.0).init()
    for i in range(100):
        a = A()
        value1 = random()
        value2 = random()
        a.a = value1
        a.b = value1
        assert a.a == a.b
        a.b = value2
        del a
        b = A()
        assert b.a == value1
        assert b.b == value2

def test_arrays(tmpdir):
    from random import random
    from numpy import zeros
    class Array():
        db = DataBase(root = tmpdir, name = 'simpledb')
        array = SavedProperty(db,'array',zeros((100,100))).init()

    a = Array()
    assert a.array.mean() == 0
    a.array += 1
    assert a.array.mean() == 1
    del a
    b = Array()
    assert b.array.mean() == 1
