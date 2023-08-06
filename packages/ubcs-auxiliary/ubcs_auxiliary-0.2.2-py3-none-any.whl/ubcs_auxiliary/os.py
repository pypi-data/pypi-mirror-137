def find(topdir, name=[], exclude=[]):
    """A list of files found starting at 'topdir' that match the patterns given
    by 'name', excluding those matching the patterns given by 'exclude'.

    Parameters
    ----------
    topdir (string)
    name (list)
    exclude (list)

    Returns
    -------
    file_list (list)

    Examples
    --------
    >>> res = anfinrud_auxiliary.os.walk('ubcs_auxiliary/')
    >>> for i in res: print(i[0])
            ...:
        ubcs_auxiliary/
        ubcs_auxiliary/tests
        ubcs_auxiliary/tests/__pycache__
        ubcs_auxiliary/__pycache__

    Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.
    In [1]: from time import time
    In [2]: import auxiliary
    In [3]: res = auxiliary.os.walk('/')
    In [4]: t1 = time(); lst = list(res); t2 = time(); print(t2-t1, len(lst))
    3.9815242290496826 1346

    Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10)
    Type "copyright", "credits" or "license" for more information.
    IPython 5.8.0 -- An enhanced Interactive Python.
    In [1]: from time import time
    In [2]: import anfinrud_auxiliary
    In [3]: res = auxiliary.os.walk('')
    In [4]: t1 = time(); lst = list(res); t2 = time(); print(t2-t1, len(lst))
    (0.77646803855896, 1346)
    """

    def glob_to_regex(pattern):
        return "^"+pattern.replace(".", "\\.").replace("*", ".*").replace("?", ".")+"$"
    try:
        from scandir import walk
    except ImportError:
        from os import walk
    import re
    if type(name) == str:
        name = [name]
    if type(exclude) == str:
        exclude = [exclude]
    name = [re.compile(glob_to_regex(pattern)) for pattern in name]
    exclude = [re.compile(glob_to_regex(pattern)) for pattern in exclude]

    file_list = []
    for (directory, subdirs, files) in walk(topdir):
        for file in files:
            pathname = directory+"/"+file
            match = any([pattern.match(pathname) for pattern in name]) and\
                not any([pattern.match(pathname) for pattern in exclude])
            if match:
                file_list += [pathname]
    return file_list

def exclude():
    """Returns a list of patterns to exclude from a search. Add
    terms as required."""
    exclude = ['*/alignment*',
               '*/trash*',
               '*/_Archived*',
               '*/backup*',
               '*/Commissioning*',
               '*/Test*',
               '*/.AppleDouble*',
               '*LaserX*',
               '*LaserZ*',
               '*Copy*',
               '*._*',
               '.DS_Store']
    return exclude

def image_file_names_from_path(beamtime,path_name):
    """Returns image file names found under path_name. Typically used with
    'Reference_*() , which specifies which directories contain data for which
    zinger-free-statistics are to be acquired. The zinger-free-statistics
    include Imean and Ivar, which are used to construct UC_psi.npy."""
    from db_functions import find,exclude
    from numpy import sort
    data_dir,analysis_dir = data_dir_analysis_dir(beamtime)
    terms = ['*.mccd','*.rx']
    image_files = sort(find(data_dir+path_name, name=terms, exclude=exclude()))
    return image_files

def N_files_in_dir(folder = '', match = '*'):
    import os
    import fnmatch
    integer = len(fnmatch.filter(os.listdir(folder), match))
    return integer

def listdir(root, include = ['.hdf5'], exclude = [], sort = ''):
    """
    returns list of files from a 'source' directory that have terms listed in 'include' and doesn't terms listed in 'exclude'. Extra parameter 'sort' can be used to sort the output list. If left blank, no sorting will be performed.

    Parameters
    ----------
    source (string)
    include (list)
    exclude (list)
    sort (string)

    Returns
    -------
    file_list (list)

    Examples
    --------
    >>> res = ubcs_auxiliary.os.get_list_of_files('/',['.hdf5'])
    """
    import os
    from numpy import argsort, array
    files = [os.path.join(root,file) for file in os.listdir(root)]
    selected = []
    [selected.append(file) for file in files if ((all([term in file for term in include])) and (all([term2 not in file for term2 in exclude])))]

    return selected

def find_recent_filename(root, include, exclude, newest_first = True):
    """
    find the list of files or folders that have any terms specified in the list 'include' and do not have terms specified in 'exclude'. The extra parameter reverse_order specified whether return the newest or oldest one.

    Parameters
    ----------
    source (string)
    include (list)
    exclude (list)
    sort (string)

    Returns
    -------
    file_list (list)
    """
    from os import listdir,path
    from os.path import getmtime
    from numpy import argsort, array
    files = [path.join(root,file) for file in listdir(root)]
    selected = []
    [selected.append(file) for file in files if ((all([term in file for term in include])) and (all([term2 not in file for term2 in exclude])))]
    path_names = selected.copy()
    if len(path_names) > 0:
        creation_times = [getmtime(file) for file in path_names]
        sort_order = argsort(creation_times)
        if newest_first:
            return array(path_names)[sort_order][-1]
        else:
            return array(path_names)[sort_order][0]
    else:
        return ''

def get_current_pid_memory_usage(units = 'GB',verbose = False):
    """
    returns current process memory footprint.
    """
    import os
    import psutil
    pid = os.getpid()
    py = psutil.Process(pid)
    coeff = 1
    if units == 'GB':
        coeff = 2.**30
    elif units == 'MB':
        coeff = 2.**20
    elif units == 'KB':
        coeff = 2.**10
    elif units == 'B':
        coeff = 2.**0.0
    elif units == 'b':
        coeff = 1.0/8.0
    memoryUse = py.memory_info()[0]/coeff  # memory use in GB...I think
    if verbose:
        print('memory use:', memoryUse)
    else:
        pass
    return memoryUse

def does_filename_have_counterpart(src_path,dst_root = None, counterpart_extension = ''):
    """
    checks if the 'src_path' has counterpart with extension 'counterpart_extension'.

    Parameters
    ----------
    filename (string)

    counterpart_extension (string)

    Returns
    -------
    boolean (boolean)
    """
    import os
    src_root, src_name = os.path.split(src_path)
    if dst_root is None:
        dst_root, dst_name = os.path.split(src_path)

    splitted = src_name.split('.')
    src_base = splitted[0]
    src_extension = ''.join(splitted[1:])
    counterpart = os.path.join(dst_root,src_base + counterpart_extension)
    flag = os.path.exists(counterpart)
    return flag


def read_config_file(filename):
    """
    read yaml config file

    Parameters
    ----------
    filename (string)

    Returns
    -------
    dict (dictionary)
    boolean (boolean)
    """
    import yaml
    import os
    flag =  os.path.isfile(filename)
    if flag:
        with open(filename,'r') as handle:
            config = yaml.safe_load(handle.read())  # (2)
    else:
        config = {}
    return config, flag
