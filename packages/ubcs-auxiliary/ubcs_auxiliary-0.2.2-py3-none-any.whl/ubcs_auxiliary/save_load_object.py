#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: Valentyn Stadnytskyi
created: Sept 9 2019

"""

def save_to_file(filename, object, protocol = 'pickle'):
    """
    save a python object to a file

    Parameters
    ----------
    Args:
        filename (string)
            the full path and filename
        object (python object)
            a python object

    Returns
    -------

    Examples
    --------
    the example of usage

    >>> save_to_file('test.pkl',[1,2,3])
    """
    if protocol =='pickle':
        from pickle import dumps
        data = dumps(object)
        with open(filename,"wb") as f:
            f.write(data)
    elif protocol == 'msgpack':
        import msgpack
        import msgpack_numpy as m
        data = msgpack.packb(object, default=m.encode)
        filename += '.msgpck'
        with open(filename,"wb") as f:
            f.write(data)
    elif protocol == 'hdf5':
        from h5py import File
        filename += '.hdf5'
        with File(filename, "w") as file:
            file.create_dataset("object", data=object)


def load_from_file(filename, protocol = 'pickle'):
    """
    read object from a file

    Parameters
    ----------
    filename : string
        the full path and filename

    Returns
    -------
    object : object
        input object to save.

    Examples
    --------
    the example of usage

    >>> list_out = load_from_file('list.extension')

    """
    if protocol == 'pickle':
        from pickle import load
        with open(filename,'rb') as f:
            data = load(f, encoding='bytes')
        return data
    elif protocol == 'hdf5':
        from h5py import File
        with File(filename, "r") as f:
            pass


def save_to_hdf5(filename, dic_in, compression = 0):
    """
    save a dictionary to a .hdf5 file

    Parameters
    ----------
    filename (string)
        the full path and filename
    dict (dictionary)
        a python dictionary
    compression (integer)
        compression paramter

    Returns
    -------

    Examples
    --------
    the example of usage

    >>> save_to_hdf5('list.hd5f',[1,2,3])
    """
    from h5py import File
    from numpy import ndarray
    with File(filename, "w") as file:
        for key in list(dic_in.keys()):
            object = dic_in[key]
            if type(object) == ndarray:
                if compression > 0:
                    file.create_dataset(key, data=object, compression = 'gzip', compression_opt = compression)
                else:
                    file.create_dataset(key, data=object)
            else:
                file.create_dataset(key, data=object)


def load_from_hdf5(filename):
    """
    read object from a file

    Parameters
    ----------
    filename : string
        the full path and filename

    Returns
    -------
    object : object
        input object to save.

    Examples
    --------
    the example of usage

    >>> data_hdf5 = load_from_hdf5('list.extension.hdf5')

    """
    from h5py import File
    from numpy import copy
    data = {}
    with File(filename, "r") as f:
        for key in list(f.keys()):
            data[key] = f[key][()]
    return data
