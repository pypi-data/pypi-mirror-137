===================
Saved Property
===================

A library provides a simple data based implementation for efficient archiving the last known values of a script. This is particularly important for python codes that are used run instruments and require certain information to be saved and available for the next run.

Start by importing UBCS LCP auxiliary package library.

first you can install the auxiliary library

.. code-block:: shell

  pip3 install ubcs_auxiliary

you may need to upgrade the library if it was installed before

.. code-block:: shell

  pip3 install --upgrade ubcs_auxiliary

>>> from ubcs_auxiliary.saved_property import DataBase, SavedProperty
>>> from  numpy import array
>>> class SomeClass():
        db = DataBase(root = tmpdir, name = 'simpledb')
        int_var = SavedProperty(db,'int_var',1).init()
        float_var = SavedProperty(db,'float_var',0.0).init()
        list_var = SavedProperty(db,'list_var',[0.0,5,6,7]).init()
        array_var = SavedProperty(db,'array_var',array([0.0,5,6,7])).init()
>>> object = SomeClass()
>>> object.int_var
  1
>>> object.int_var = 3
>>> object.float_var
  0.0
>>> object.float_var = 5.7
>>> del object
>>> object2 = SomeClass()
>>> print( object2.int_var, object2.float_var)
  (3,5.7)


.. autoclass:: ubcs_auxiliary.saved_property.DataBase
  :members:

  .. automethod:: __init__

.. autoclass:: ubcs_auxiliary.saved_property.SavedProperty
  :members:

  .. automethod:: __init__
