def compress_file(filename, compressoin = 0, retain = False):
    """
    a function that recompresses the hdf5 file.
    """
    from time import ctime, time
    import os


def compress_files(dir, compressoin = 0, retain = False):
    import os
    from time import time, ctime
    src_lst = os.listdir()
    dest_lst = []
    for item in src_lst:
        if retain:
            flag = '.hdf5' in item  and '.hdf5.gzip9' not in item
        else:
            flag = '.hdf5' in item
        if flag:
            dest_lst.append(item)
    print(dest_lst)
    for item in dest_lst:
        src_file = item
        dst_file = item+'.gzip9'
        print('start',ctime(time()))
        os.system(f'h5repack -v {src_file} {dst_file} GZIP=9')
        if not retain:
            os.remove(src_file)
        print('end',ctime(time()))
