"""
plotting functions
author: Valentyn Stadnytskyi
data: 2017 - Nov 17 2018

"""
__vesrion__ = '1.0.0'
from time import  time, sleep
import sys
if sys.version_info[0] == 2:
    from time import clock as perf_counter
else:
    from time import perf_counter
import platform
from numpy import asarray

### Mathematical Functions
def exponential_1(x,x0,A,tau, offset):
    """
    exponential function with one exponent
    """
    from numpy import exp
    func = A*exp(-(x-x0)/tau)+offset
    return func

def linear(x,a,b):
    """
    linear function
    """
    return a + b*x

def binary_to_array(value = 0, length = 8):
    """
    takes an integer and converts it to 8 bit representation as an array.
    If float number is passed, it will be converted to int.
    """
    from numpy import arange,ndarray,nan
    value = int(value)
    binary = format(value, '#0'+str(length+2)+'b')
    arr = arange(length-1)
    for i in range(length-1):
        arr[i] = binary[length+1-i]
    return arr

def array_to_binary(arr = asarray([ 1,  1,  1,  1,  1,  1,  1])):
    """
    takes an integer and converts it to 8 bit representation as an array.
    If float number is passed, it will be converted to int.
    """
    from numpy import arange,ndarray,nan
    integer = 0
    for i in range(len(arr)):
        integer += int(arr[i]*2**(i))
    return integer

def bin_data(data  = None, x = None, axis = 1, num_of_bins = 300, dtype = 'float'):
        """returns a vector of integers on logarithmic scale starting from decade start, ending decade end with M per decade
        Parameters
        ----------
        data (numpy array)
        x (numpy array)
        axis (integer)
        num_of_bins (integer)
        dtype (string)

        Returns
        -------
        dictionary with keys: 'x',y_min','y_max''y_mean'

        Examples
        --------
        >>> from numpy import random, arange
        >>> data = random.rand(4,1000)+ 1
        >>> x_in = arange(0,data.shape[0]+1,1)
        >>> binned_data = bin_data(data  = None, x = None, axis = 1, num_of_bins = 300, dtype = 'float')

        .. plot:: ./examples_py/numerical_bin_data.py
           :include-source:

        """
        from numpy import zeros, nan,arange, nanmax, nanmin, random,nanmean, mean
        import math
        if len(data.shape) > 1:
            length = data.shape[0]
            width = data.shape[1]
        else:
            length = data.shape[0]
            width = 1

        if x is None:
            x = arange(0,length,1)

        if length <= num_of_bins:
            y_max = data
            y_min = data
            y_mean = data
            x_out = x
        else:
            y_min = zeros(shape = (width,num_of_bins), dtype = dtype)
            y_max = zeros(shape = (width,num_of_bins), dtype = dtype)
            y_mean = zeros(shape = (width,num_of_bins), dtype = dtype)
            x_out = zeros(shape = (num_of_bins,), dtype = dtype)

            for j in range(width):
                idx = 0
                for i in range(num_of_bins):
                    step = int(math.ceil(1.0*(length - idx)/(num_of_bins-i)))

                    start = idx
                    end = idx + step
                    if 'int' in dtype:
                        y_max[j,i] = int(nanmax(data[start:end,j]))
                        y_mean[j,i] = int(nanmean(data[start:end,j]))
                        y_min[j,i] = int(nanmin(data[start:end,j]))
                    else:
                        y_max[j,i] = nanmax(data[start:end,j])
                        y_mean[j,i] = nanmean(data[start:end,j])
                        y_min[j,i] = nanmin(data[start:end,j])
                    x_out[i] = mean(x[start:end])
                    idx += step
        dic = {}
        dic['x'] = x_out
        dic['y_min'] = y_min
        dic['y_max'] = y_max
        dic['y_mean'] = y_mean
        return dic

def bin_xy(y  = None, x = None, axis = 1, num_of_bins = 300, dtype = 'float'):
        """returns a vector of integers on logarithmic scale starting from decade start, ending decade end with M per decade
        Parameters
        ----------
        data (numpy array)
        x (numpy array)
        axis (integer)
        num_of_bins (integer)
        dtype (string)

        Returns
        -------
        dictionary with keys: 'x',y_min','y_max''y_mean'

        Examples
        --------
        >>> from numpy import random, arange
        >>> data = random.rand(4,1000)+ 1
        >>> x_in = arange(0,data.shape[0]+1,1)
        >>> binned_data = bin_data(data  = None, x = None, axis = 1, num_of_bins = 300, dtype = 'float')

        .. plot:: ./examples_py/numerical_bin_data.py
           :include-source:

        """
        from numpy import zeros, nan,arange, nanmax, nanmin, random,nanmean, mean
        import math

        length = y.shape[0]


        if length <= num_of_bins:
            y_max = data
            y_min = data
            y_mean = data
            x_out = x
        else:
            y_min = zeros(shape = (num_of_bins,), dtype = dtype)
            y_max = zeros(shape = (num_of_bins,), dtype = dtype)
            y_mean = zeros(shape = (num_of_bins,), dtype = dtype)
            x_out = zeros(shape = (num_of_bins,), dtype = dtype)

            idx = 0
            for i in range(num_of_bins):
                step = int(math.ceil(1.0*(length - idx)/(num_of_bins-i)))
                start = idx
                end = idx + step
                if 'int' in dtype:
                    y_max[i] = int(nanmax(y[start:end]))
                    y_mean[i] = int(nanmean(y[start:end]))
                    y_min[i] = int(nanmin(y[start:end]))
                else:
                    y_max[i] = nanmax(y[start:end])
                    y_mean[i] = nanmean(y[start:end])
                    y_min[i] = nanmin(y[start:end])
                x_out[i] = mean(x[start:end])
                idx += step
        dic = {}
        dic['x'] = x_out
        dic['y_min'] = y_min
        dic['y_max'] = y_max
        dic['y_mean'] = y_mean
        return dic

def sort_vector(in_vector = asarray([ 1,  1,  1,  1,  1,  1,  1])):
    """sorts time vector"""
    from numpy import sort
    if in_vector.ndim == 1:
        out_vector = sort(in_vector)
    return out_vector

def expand_vector(in_vector = asarray([ 1,  1,  1,  1,  1,  1,  1]),ndim = 2):
    """ makes input 1D vector as 2D with first dimenstion to be ndim"""
    from numpy import zeros,expand_dims,concatenate
    out_vector = expand_dims(in_vector, axis = 0)
    add_vector = out_vector*0
    for i in range(ndim-1):
        out_vector = concatenate((out_vector,add_vector),axis=0)
        return out_vector

def get_estimate(x,y,x_est, order = 2):
        """
        returns estimated y_est value for give x_est from real x,y data set.
        """
        from numpy import polyfit, poly1d, nanargmin
        idx = nanargmin((x - x_est)**2)
        x0 = x[idx]
        debug('x = %r' %x)
        debug('y = %r' %y)
        debug('x_est = %r' %y)
        debug('idx = %r' %idx)
        debug('x0 = %r' %x0)
        if len(x) !=0 or len(y) != 0:
            fit = polyfit(x-x0,y,order)
            ynew_fit = poly1d(fit)(x_est-x0)
        else:
            ynew_fit = nan
        return ynew_fit

def log_scale(N = 8, start = -9, end = 3, round_to = 3):
    """creates an array of numbers on logarithmic scale with:
        - number per decade
        - start decade
        - end decade
        - round_to number of digits after decimal, default is 3
        """
    from numpy import logspace, around
    arr = around(logspace(start,  end, (end-start)*N+1, endpoint=True),abs(start-round_to))
    return arr

def local_log_scale(start_dec, end_dec, N_per_dec, dtype = 'int64'):
    """returns a vector of integers on logarithmic scale starting from decade start, ending decade end with M per decade
    Parameters
    ----------
    start_dec (integer)
    end_dec (integer)
    N_per_dec (integer)
    dtype (string)

    Returns
    -------
    array (numpy array)

    Examples
    --------
    >>> arr = local_log_scale(start_dec = -9, end_dec = 1, N_per_dec = 4, dtype = 'int64')
    """
    from numpy import logspace, around
    arr = logspace(start_dec,  end_dec, (end_dec-start_dec)*N_per_dec, endpoint=False,dtype = dtype)
    return arr

def bin_on_logscale(x,y,N = 100, dN = 1, x0 = 0, M = 16, order = 1, mode = 'polyfit'):
    """
    purpose: binning of data: first N points starting from x0 are
    binned in bins of size dN and the rest is binned on logarithmic scale with M per decade

    Parameters
    ----------
    x (integer) - x-axis of data
    y (integer) - y-axis of data
    x0 (float) - the zero on x-axis
    N (int) - number of points after x0 that are binned , dN bi size, on linear scale
    dN (integer) - size of the bin for the linear scale, first N points.
    M (integer)- number of points per decade for the rest of the data

    Returns
    -------
    (y_mean, y_std, x_out, num)
    y_mean array (numpy array)
    y_std  array (numpy array)
    x_out  array (numpy array)
    num array (numpy array)

    Examples
    --------
    >>> arr = local_log_scale(start_dec = -9, end_dec = 1, N_per_dec = 4, dtype = 'int64')
    """
    if M >128:
        raise ValueError('Value of M = %r has exceeded allowed (%r)' %(M,128))

    def lin_func(x_l,x_r,y,x0, order = 2, fit_mode = 'mean'):
        """
        """
        from numpy import polyfit, poly1d, arange, std
        if y.shape[0] > 1:
            x = arange(x_l,x_r,1)
            if x.shape[0] >2:
                if fit_mode == 'polyfit':
                    #print('1',fit_mode)
                    y_fit = poly1d(polyfit(x,y,deg = order))
                    y_fit_x0 = y_fit(x0)
                    y_std = (sum((y_fit(x) - y)**2)/x.shape[0])**0.5
                elif fit_mode == 'bevington':
                    #print('2',fit_mode)
                    a,b,y_std = linear_fit(x,y)
                    y_fit_x0 = linear(x0,a,b)
                else:
                    #print('3',fit_mode)
                    y_fit_x0,y_std = mean(y), std(y)
            else:
                if fit_mode == 'polyfit':
                    y_fit = poly1d(polyfit(x,y,deg = 1))
                    y_fit_x0 = y_fit(x0)
                    y_std = (sum((y_fit(x) - y)**2)/x.shape[0])**0.5
                elif fit_mode == 'bevington':
                    a,b,y_std = linear_fit(x,y)
                    y_fit_x0 = linear(x0,a,b)
                else:
                    y_fit_x0,y_std = mean(y), std(y)


            return y_fit_x0, y_std
        else:
            return y, 0
    t={}
    k = 0
    t0 = time()

    from numpy import mean, std, arange, argwhere, concatenate,polyfit, poly1d, mod, log10
    y = transpose(y)
    x_len = x.shape[0]
    y_len = y.shape[0]
    num = x_len
    t[k] = time() - t0;k +=1;
    lin_left = arange(0,(N-1)*dN,dN)
    lin_right = arange(dN,N*dN,dN)
    lin_middle = lin_left/2.0+(lin_right-1)/2.0
    #print('lin_left.shape[0] = %r. lin_right.shape[0] = %r' %(lin_left.shape[0], lin_right.shape[0]))
    t[k] = time() - t0;k +=1;
    up_to = int(log10(num))+1
    x_log = local_log_scale(1,up_to,2*M)
    arr1  = x_log[argwhere((x_log >= lin_right[-1]))][:,0]
    arr2 = arr1[argwhere(arr1 <= x_len)][:,0]
    log_left = arr2[asarray(range(0,arr2.shape[0],2))]
    log_middle = arr2[asarray(range(1,arr2.shape[0],2))]
    log_right = arr2[asarray(range(2,arr2.shape[0],2))]
    t[k] = time() - t0;k +=1;
    right = concatenate((lin_right,log_right))
    left = concatenate((lin_left,log_left))[:len(right)]
    middle = concatenate((lin_middle,log_middle))[:len(right)]

    t[k] = time() - t0;k +=1;
    x_out = right*0.0
    y_mean = right*0.0
    y_std = right*0.0
    num = right*0.0
    #print(bogus)
    t[k] = time() - t0;k +=1;
    for i in range(x_out.shape[0]):
        #if mod(N,2):
        x_out[i],x_out_std = lin_func(left[i],right[i],x[left[i]:right[i]],middle[i], order = order, fit_mode = 'polyfit')
        #else:
           # try: x_out[i] = x[int(middle[i])]
           # except: print('bla');x_out[i] = x[int(middle[i])-1]
        y_mean[i],y_std[i] = lin_func(left[i],right[i],y[left[i]:right[i]],middle[i], order = order, fit_mode = mode)
        num[i] = x[left[i]:right[i]].shape[0]
    t[k] = time() - t0;k +=1;
    return y_mean, y_std, x_out, num


def linear_fit(x,y):
    """
    return linear fit by calcualating
    y_fit = a + b*x
    page 104 Data reduction and error analysis for the physicxal sciences Philip R. Bevington

    Parameters
    ----------
    x (1d numpy array)
    y (1d numpy array)

    Returns
    -------
    a
    b
    sigma

    Examples
    --------
    >>> a, b , sigma = linear_fit(x,y)
    """

    from numpy import isnan,nan, sum

    Sx = sum(x*1.0) #Sx_i = Sx_i-1 +x_i
    Sx2 = sum(x**2.00) #Sx2_i = Sx2_i-1 + x_i**2
    Sy = sum(y*1.0) #Sy_i = Sy_i-1 + y_i
    Sy2 = sum(y**2.0) #Sy2_i = Sy2_i-1 + y_i**2
    Sxy = sum(x*y*1.0) #Sxy_i = Sxy_i-1 + x_i*y_i
    N = x.shape[0]#N_i = N_i-1 + 1.0
    if N >= 2:
        Delta = N*Sx2 - Sx**2 # Delta_i = N_i*Sx2_i - Sx_i**2
        a = (1.0/Delta)*(Sx2*Sy-Sx*Sxy)
        b = (1.0/Delta)*(N*Sxy-Sx*Sy)
    else:
        a = None
        b = None
        #page 115
    if N > 2:
        Sigma = (1/(N-2))*(Sy2+N*a**2+(b**2)*Sx2-2*a*Sy-2*b*Sxy+2*a*b*Sx)
    else:
        Sigma = None

    return a, b, Sigma

def weighted_linear_fit(x,y,w):
    """
    return linear fit by calcualating
    y_fit = a + b*x
    page 104 Data reduction and error analysis for the physicxal sciences Philip R. Bevington

    Parameters
    ----------
    x (1d numpy array)
    y (1d numpy array)
    w (1d numpy array)

    Returns
    -------
    a
    b
    sigma_a
    sigma_b

    Examples
    --------
    >>> a, b , sigma_a, sigma_v = weighted_linear_fit(x,y,w)
    """

    from numpy import isnan,nan, sum, sqrt, min, max
    coeff = abs(x.min()-x.max())
    x = x/coeff
    Sx = sum(w*x*1.0) #Sx_i = Sx_i-1 +x_i
    Sx2 = sum(w*x**2.0) #Sx2_i = Sx2_i-1 + x_i**2
    Sy = sum(w*y*1.0) #Sy_i = Sy_i-1 + y_i
    Sy2 = sum(w*y**2.0) #Sy2_i = Sy2_i-1 + y_i**2
    Sxy = sum(w*x*y*1.0) #Sxy_i = Sxy_i-1 + x_i*y_i
    Sw = sum(w)
    N = x.shape[0]#N_i = N_i-1 + 1.0
    if N >= 2:
        Delta = (Sw*Sx2 - Sx**2) # Delta_i = N_i*Sx2_i - Sx_i**2
        a = (1.0/Delta)*(Sx2*Sy-Sx*Sxy)*coeff**2
        b = (1.0/Delta)*(Sw*Sxy-Sx*Sy)*coeff
    else:
        a = None
        b = None
        #page 115
    if N > 2:
        sigma_a = sqrt((1/Delta)*Sx2)
        sigma_b = sqrt((1/Delta)*Sw/coeff**2)
    else:
        sigma_a = sigma_b = None
    print('Delta = ',Delta)
    print('Sw2 = ',Sw)
    print('Sx = ',Sx)
    print('Sx2 = ',Sx2)
    print('coeff = ',coeff)
    print('sigma_a = ',sigma_a)
    print('sigma_b = ',sigma_b)

    return a, b, sigma_a, sigma_b

def interpolate(x,y,x_new,w = None,s = None,):
    from scipy.interpolate import UnivariateSpline
    spl = UnivariateSpline(x, y)
    y_new = spl(x_new)

def weighted_linear_fit_test_data():
    from numpy import arange, array,sqrt
    x = 5 + arange(0,150,15)/coeff
    y = array([106,80,98,75,74,73,49,38,37,22])
    w = 1/y
    return x,y,w

def weighted_linear_fit_test():
    from numpy import sqrt
    x,y,w = weighted_linear_fit_test_data()
    a,b,sigma_a,sigma_b = weighted_linear_fit(x,y,w)
    plt.figure()

    plt.errorbar(x,y,1/sqrt(w),marker='s')
    plt.plot(x,a+b*x)
    string = str(round(a,3))+','+str(round(b,3))+','+str(round(sigma_a,3))+','+str(round(sigma_b,3))
    plt.errorbar(x0,a+b*(x0),sqrt(sigma_a**2+(x0*sigma_b)**2),marker = 's')
    string += ','+str(round(sqrt(sigma_a**2+(x0*sigma_b)**2),3))
    plt.title(string)
    plt.show()
    return [sqrt(sigma_a**2+(x0*sigma_b)**2),x.max()-x.min()]

def grow_mask(mask, count=1):
    """
    Expands area where pixels have value=1 by 'count' pixels in each
    direction, including along the diagonal.

    Example: If count is 1 or omitted a single pixel grows to nine pixels.

    Parameters
    ----------
    mask (2d numpy array)
    count (integer)

    Returns
    -------
    mask (2d numpy array)

    Examples
    --------
    >>>  mask2 = grow_mask(mask,2)
    """
    from numpy import array,zeros

    if count < 1: return mask
    if count > 1: mask = grow_mask(mask,count-1)
    w,h = mask.shape
    mask2 = zeros((w,h),mask.dtype)
    mask2 |= mask
    mask2[0:w,0:h-1] |= mask[0:w,1:h] # move up by 1 pixel
    mask2[0:w,1:h] |= mask[0:w,0:h-1] # move down by 1 pixel
    mask2[0:w-1,0:h] |= mask[1:w,0:h] # move to the left by 1 pixel
    mask2[1:w,0:h] |= mask[0:w-1,0:h] # move to the right by 1 pixel

    mask2[0:w-1,0:h-1] |= mask[1:w,1:h] # move left and up by 1 pixel
    mask2[0:w-1,1:h] |= mask[1:w,0:h-1] # move left and down by 1 pixel
    mask2[1:w,0:h-1] |= mask[0:w-1,1:h] # move up and up by 1 pixel
    mask2[1:w,1:h] |= mask[0:w-1,0:h-1] # move up and down by 1 pixel

    return mask2

def enumerate_mask(mask, value = 1):
    """
    Takes a boolean mask, enumerates spots and returns enumerated mask where the intensity of a pixel indicates the spot number.
    """
    from skimage import measure
    emask = measure.label(mask==value)
    return emask

def get_array_piece(arr, center = (0,0), radius = 15, dtype = 'uint16'):
    """
    grabs a square box around center with given radius. Note that first entry in center is x coordinate (or cols) and second is y (rows)

    Example: center = (100,100) and radirus = 15.
    return array will contain data with shape (31,31) centered at pixel (100,100).
    """
    from numpy import nan,zeros,array
    x, y = center
    r = radius
    flag1 = ((x+r) < arr.shape[1])
    flag2 = ((y+r) < arr.shape[0])
    flag3 = ((x-r) > 0)
    flag4 = ((y-r) > 0)
    if flag1*flag2*flag3*flag4:
        result = arr[y-r:y+r+1,x-r:x+r+1]
    else:
        result = zeros((2*r+1,2*r+1))
        for idx in range(2*r+1):
            for idy in range(2*r+1):
                isx = x-r+idx
                isy = y-r+idy
                if (isx < arr.shape[1]) and (isy < arr.shape[0]) and (isx >= 0) and (isy >= 0):
                    result[idy,idx] = arr[isy,isx]
                else:
                    result[idy,idx] = 0

    return result

def get_random_array(size = (3000,4096),range = (0,4094), dtype = 'uint16'):
    """
    returns random array
    """
    from numpy.random import randint
    if dtype == 'uint16':
        arr = randint(range[0],range[1],size = size,dtype = dtype)
    else:
        arr = randint(range[0],range[1],size = size,dtype = dtype)
    return arr

def return_noise(size = (10,10), mean = 15, variance = 2, dtype = 'uin16'):
    """
    returns an numpy array with given size, mean value and variance. If dtype
    """
    from numpy.random import normal
    from numpy import sqrt
    noise = normal(loc=mean, scale=sqrt(variance), size=size).astype(dtype)
    return noise

def get_histogram(arr,length = 16,step = 1):
    """
    assumes unsigned int 16
    """
    from numpy import arange, histogram
    bins = arange(0,length,step) #calculating histogram
    y,x = histogram(arr,bins = bins)
    return x[:-1],y

def gaussian2D_from_shape(shape = (100,100), amplitude = 3000, position = (100,100), sigma = (5,5), dtype = 'uint16'):
    """
    return 2D gaussian function in a given 'position' on the provided image. The input image can be made of all zeros.
    """
    from numpy import sqrt,exp,copy,zeros
    r_mu = position[0]
    c_mu = position[1]
    r_sigma = sigma[0]
    c_sigma = sigma[1]
    gaussian = zeros(shape = shape)
    for r in range(gaussian.shape[0]):
        for c in range(gaussian.shape[1]):
            gaussian[r,c] = amplitude*exp(-((r-r_mu)**2/(2.0*r_sigma**2))-( (c-c_mu)**2 /( 2.0 * c_sigma**2) ) )

    return gaussian.astype(dtype)

def bin_array(num, m):
    from numpy import uint8, binary_repr,array
    """Convert a positive integer num into an m-bit bit vector"""
    return array(list(binary_repr(num).zfill(m))).astype(uint8)

def binarr_to_number(vector):
    """
    converts a vector of bits into an integer.
    """
    num = 0
    from numpy import flip
    vector = flip(vector)
    length = vector.shape[0]
    for i in range(length):
       num += (2**(i))*vector[i]
    return num

def nonzeromax(arr):
    """
    returns non-zero and nan maximum of a given array.
    """
    from numpy import nanmax, where
    idx = where(arr != 0)
    if idx[0].shape[0] > 0:
        return nanmax(arr[idx])
    else:
        return None

def nonzeromin(arr):
    """
    returns non-zero and nan minimum of a given array.
    """
    from numpy import nanmin, where
    idx = where(arr != 0)
    if idx[0].shape[0] > 0:
        return nanmin(arr[idx])
    else:
        return None

def gaussian1D(x, amp, x0, sigma, offset):
    """
    simple one-dimensional gaussian function
    """
    from numpy import exp
    y = amp*exp(-(x-x0)**2/(2*sigma*sigma))
    return y

def gaussian2D_from_mesh(mesh, amplitude, x0, y0, x_sigma, y_sigma, offset = 0 , theta = 0):
    """
    returns two-dimensional gaussian

    Parameters
    ----------
    mesh (2d numpy array)
    amplitude (float)
    x0 (float)
    y0 (float)
    x_sigma (float)
    y_sigma  (float)
    offset (float)
    theta (float)

    Returns
    -------
    z (2d numpy array)

    Examples
    --------
    >>> x = np.linspace(0, 20, 21)
    >>> y = np.linspace(0, 20, 21)
    >>> x,y = np.meshgrid(x, y)
    >>> xy = (x,y)
    >>> amp, x0, y0, sigmax, sigmay,offset, theta = 100,10,10,3,3,0,0
    >>> z = gaussian2D_from_mesh(xy,amp,x0,y0,sigmax,sigmay,offset)
    """
    from numpy import cos, sin, exp
    x = mesh[0]
    y = mesh[1]
    a = (cos(theta)**2)/(2*x_sigma**2) + (sin(theta)**2)/(2*y_sigma**2)
    b = -(sin(2*theta))/(4*x_sigma**2) + (sin(2*theta))/(4*y_sigma**2)
    c = (sin(theta)**2)/(2*x_sigma**2) + (cos(theta)**2)/(2*y_sigma**2)
    z = offset + amplitude*exp( - (a*((x-x0)**2) + 2*b*(x-x0)*(y-y0) + c*((y-y0)**2)))
    return z

def noise(arr,mean,sigma):
    """
    returns normal distributed noise array
    of shape x with mean and sigma.
    """
    from numpy.random import normal
    result = normal(mean,sigma,arr.shape)
    return result

def pixelate_xy(x,y,pixel_length = 10, dtype = None, saturation_value = None):
    """
    returns pixelated x,y-data. The length of x and y has to be divisable by pixel_size.
    """
    from numpy import zeros
    x_len = x.shape[0]
    y_len = y.shape[0]

    if x_len != y_len:
        raise ValueError('The shape of x and y input vectors has to be the same')

    if (x_len%pixel_length)!=0 or (y_len%pixel_length)!=0:
        raise ValueError('The length of the input data arrays has to be divisable by pixel_length')

    if dtype is None:
        x_dtype = x.dtype
        y_dtype = y.dtype
    else:
        x_dtype = dtype
        y_dtype = dtype

    x_new_len = int(x_len/pixel_length)
    y_new_len = int(y_len/pixel_length)
    x_new = zeros((x_new_len,), dtype = x_dtype)
    y_new = zeros((y_new_len,), dtype = y_dtype)
    for i in range(int(x_new_len)):
        x_new[i] = x[i*pixel_length:(i+1)*pixel_length].mean()
        y_new[i] = y[i*pixel_length:(i+1)*pixel_length].mean()
    if saturation_value is not None:
        y_new[y_new>=saturation_value] = saturation_value
    return x_new,y_new

def pixelate_image(x,y,z,pixel_size = 10, saturation_value = None):
    """
    returns pixilated image with pixel_size as input.
    The shape has to be divisible by pixel_size

    .. math::

        z =

    Parameters
    ----------
    mesh (2d numpy array)
    amplitude (float)
    x0 (float)
    y0 (float)
    x_sigma (float)
    y_sigma  (float)
    offset (float)
    theta (float)

    Returns
    -------
    z (2d numpy array)

    Examples
    --------
    >>> x = np.linspace(0, 20, 21)
    >>> y = np.linspace(0, 20, 21)
    >>> x,y = np.meshgrid(x, y)
    >>> xy = (x,y)
    >>> amp, x0, y0, sigmax, sigmay,offset, theta = 100,10,10,3,3,0,0
    >>> z = gaussian2D_from_mesh(xy,amp,x0,y0,sigmax,sigmay,offset)
    """
    from numpy import zeros
    x_shape = x.shape[0]
    y_shape = y.shape[0]
    z_shape = z.shape[0]
    x_new_len = int(x_shape/pixel_size)
    y_new_len = int(y_shape/pixel_size)
    z_new_len = int(z_shape/pixel_size)
    x_new = zeros((x_new_len,x_new_len))
    y_new = zeros((y_new_len,y_new_len))
    z_new = zeros((z_new_len,z_new_len))
    for i in range(int(x_new_len)):
        for j in range(int(x_new_len)):
            y_new[i,j] = y[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size].mean()
            x_new[i,j] = x[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size].mean()
            z_new[i,j] = z[i*pixel_size:(i+1)*pixel_size,j*pixel_size:(j+1)*pixel_size].mean()
    if saturation_value is not None:
        z_new[z_new>=saturation_value] = saturation_value
    return x_new,y_new,z_new

def nearest_neibhour(row,col):
    """
    returns an matrix of indices where fast axis (axis = 0) corresponds to particle index and the resulting vector show the order of nearest neibhours.


    Parameters
    ----------
    row (1d numpy array)
    col (1d numpy array)
    Returns
    -------
    matrix (2d numpt array)

    Examples
    --------
    >>> import numpy as np
    >>> row = np.asarray([100, 200,400, 600, 150])
    >>> col = np.asarray([100, 200,300, 400, 300])
    >>> nn = nearest_neibhour(row = row,col = col)
    >>> nn
    array([[0, 1, 4, 2, 3],
       [1, 4, 0, 2, 3],
       [2, 1, 3, 4, 0],
       [3, 2, 1, 4, 0],
       [4, 1, 0, 2, 3]])

    >>> print("and visualy can be represented as a scatter chart, where the marker is replaced with a closest neibhours. 0 - stands for the point for which neibhours are calculated.")"

    .. plot::

        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> from ubcs_auxiliary import numerical
        >>> row = np.asarray([100, 200,400, 600, 150])
        >>> col = np.asarray([100, 200,300, 400, 300])
        >>> nn = numerical.nearest_neibhour(row = row, col = col)
        >>> plt.grid()
        >>> for i in range(len(nn[1])):
        >>>    plt.scatter(col[nn[1,i]],row[nn[1,i]], s=400, marker = f'${i}$')
        >>> plt.title('example: point 1')
        >>> plt.show()

    """
    from numpy import zeros, nan, nanmin, amin, ones, sqrt, where, argsort

    matrix = distance_matrix(row,col)
    matrix_argsort = argsort(matrix,axis=1)
    return matrix_argsort

def distance_matrix(row,col):
    """
    returns a matrix of all pair-wise distances.

    Parameters
    ----------
    row (1d numpy array)
    col (1d numpy array)
    Returns
    -------
    matrix (2d numpt array)

    Examples
    --------
    >>> import numpy as np
    >>> row = np.asarray([100,200,400])
    >>> col = np.asarray([100,200,300])
    >>> dist = distance_matrix(row = row,col = col)
    >>> dist
    array([[  0.        , 141.42135624, 360.55512755],
       [141.42135624,   0.        , 223.60679775],
       [360.55512755, 223.60679775,   0.        ]])
    """
    from numpy import zeros, meshgrid,sqrt
    # vectorized form, might use more RAM
    row_i, row_j = meshgrid(row, row, sparse=True)
    row_m = ((row_i-row_j)**2)
    col_i, col_j = meshgrid(col, col, sparse=True)
    col_m = ((col_i-col_j)**2)
    matrix = sqrt(row_m + col_m)
    del col_m, row_m, row_i, row_j,col_i, col_j
    return matrix

def linear_coeff_from_points(p1,p2):
    """
    p1(x1,y1)
    p2(x2,y2)

    y = a*x+b
    """
    y1 = p1[1]
    y2 = p2[1]
    x1 = p1[0]
    x2 = p2[0]

    a = (y1-y2)/(x1-x2)
    b = (x1/(x1-x2))*(y1-y2) + y1
    return a,b

def max_filter(image, footprintsize = 10, treshhold = 100):
    """
    returns mask with max values with given distance

    to find the mask of max pixels. These are peak pixels in the image.
    """
    from scipy.ndimage import maximum_filter
    from numpy import ones
    footprint = ones((footprintsize,footprintsize))
    max_mask = (maximum_filter(image,footprint = footprint) == image)&(image>=treshhold)

    return max_mask
