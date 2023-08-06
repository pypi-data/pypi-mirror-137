from numpy import zeros, array_equal

from ubcs_auxiliary.save_load_object import save_to_file,  load_from_file

def test_save_load(tmpdir):
    import os
    print(f'tempdir = {tmpdir}')
    print(f'{os.path.exists(tmpdir)}')
    arr_in = zeros((10,5))
    str_in = 'this is string'
    dict_in = {'1':1,'2':2}
    list_in = [1,2,3,4]
    compound_in = {}
    compound_in['arr'] = arr_in
    compound_in['str'] = str_in
    compound_in['dict'] = dict_in
    compound_in['list'] = list_in

    # save to a file
    save_to_file(tmpdir+'/arr.pkl',arr_in)
    save_to_file(tmpdir+'/str.pkl',str_in)
    save_to_file(tmpdir+'/dict.pkl',dict_in)
    save_to_file(tmpdir+'/list.pkl',list_in)
    save_to_file(tmpdir+'/compound.pkl',compound_in)

    # Load to a file
    arr_out = load_from_file(tmpdir+'/arr.pkl')
    str_out = load_from_file(tmpdir+'/str.pkl')
    dict_out = load_from_file(tmpdir+'/dict.pkl')
    list_out = load_from_file(tmpdir+'/list.pkl')
    compound_out = load_from_file(tmpdir+'/compound.pkl')

    #run tests
    assert array_equal(arr_in, arr_out)
    assert str_in == str_out
    assert dict_in == dict_out
    assert list_in == list_out
    assert compound_in.keys() == compound_out.keys()

def test_save_load_hdf5(tmpdir):
    from ubcs_auxiliary.save_load_object import save_to_hdf5,  load_from_hdf5
    import os
    print(f'tempdir = {tmpdir}')
    print(f'{os.path.exists(tmpdir)}')
    arr_in = {'array':zeros((10,5))}
    str_in = {'string':b'this is string'}
    dict_in = {'1':1,'2':2}
    list_in = {'list':[1,2,3,4]}
    compound_in = {}
    compound_in['array'] = arr_in['array']
    compound_in['string'] = str_in['string']
    compound_in['list'] = list_in['list']

    # save to a file
    save_to_hdf5(tmpdir+'/arr.hdf5',arr_in)
    save_to_hdf5(tmpdir+'/str.hdf5',str_in)
    save_to_hdf5(tmpdir+'/dict.hdf5',dict_in)
    save_to_hdf5(tmpdir+'/list.hdf5',list_in)
    save_to_hdf5(tmpdir+'/compound.hdf5',compound_in)

    # Load to a file
    arr_out = load_from_hdf5(tmpdir+'/arr.hdf5')
    str_out = load_from_hdf5(tmpdir+'/str.hdf5')
    dict_out = load_from_hdf5(tmpdir+'/dict.hdf5')
    list_out = load_from_hdf5(tmpdir+'/list.hdf5')
    compound_out = load_from_hdf5(tmpdir+'/compound.hdf5')

    #run tests
    assert array_equal(arr_in['array'], arr_out['array'])
    assert str_in == str_out
    assert dict_in == dict_out
    print('lists',list_in,list_out)
    #Note HDF5 returns a saved list as an array
    assert list_in['list'] == list(list_out['list'])
    assert compound_in.keys() == compound_out.keys()
