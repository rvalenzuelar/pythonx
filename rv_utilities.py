'''
    Utility functions

    Raul Valenzuela
    raul.valenzuela@colorado.edu
'''


def add_colorbar(ax, im, cbar_ticks=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    if cbar_ticks is None:
        cbar = plt.colorbar(im, cax=cax)
    else:
        cbar = plt.colorbar(im, cax=cax, ticks=cbar_ticks)
    return cbar


def format_xaxis(ax, time_array, delta_hours=3):
    import numpy as np
    ' time is start hour'
    date_fmt = '%d\n%H'
    new_xticks = np.asarray(range(len(time_array)))
    xtlabel = []
    for t in time_array:
        if np.mod(t.hour, delta_hours) == 0:
            xtlabel.append(t.strftime(date_fmt))
        else:
            xtlabel.append('')
    ax.set_xticks(new_xticks)
    ax.set_xticklabels(xtlabel)


def format_yaxis(ax, hgt, **kwargs):
    ''' assumes hgt in km '''
    import numpy as np
    from scipy.interpolate import interp1d
    if 'toplimit' in kwargs:
        ''' extentd hgt to toplimit km so all
        time-height sections have a common yaxis'''
        toplimit = kwargs['toplimit']
        hgt_res = np.unique(np.diff(hgt))[0]
        hgt = np.arange(hgt[0], toplimit, hgt_res)
    f = interp1d(hgt, range(len(hgt)))
    first_gate = np.ceil(hgt[0]*100)/100
    last_gate = np.ceil(hgt[-1]*100)/100
    resolution = 0.2
    ys = np.arange(first_gate, last_gate, resolution)
    new_yticks = f(ys)
    ytlabel = ['{:2.2f}'.format(y) for y in ys]
    ax.set_yticks(new_yticks + 0.5)
    ax.set_yticklabels(ytlabel)


def pandas2stack(pandas_array):
    ''' converts pandas dataframe containing
    t rows of 2D (m x n) arrays to a numpy 3D
    array of dimensions (m x n x t) '''
    import numpy as np
    narrays = pandas_array.shape[0]
    for n in range(narrays):
        a = pandas_array.iloc[[n]].values[0]
        if isinstance(a, list):
            a = np.array(a)
        if n == 0:
            A = a.copy()
        else:
            A = np.dstack((A, a))
    return A

def fill2D_with_nans(inarray=None, start=[None,None], 
                    size=[None,None]):


    outarray = inarray.copy().astype(float)

    ' for each column'
    for i,c in enumerate(inarray.T):
        out = fill1D_with_nans(inarray=c,
                                start=start[0],
                                size=size[0])
        outarray[:,i]=out

    ' for each row'
    for i,c in enumerate(outarray):
        out = fill1D_with_nans(inarray=c,
                                start=start[1],
                                size=size[1])
        outarray[i,:]=out

    return outarray

def fill1D_with_nans(inarray=None, start=None, size=None):
    import numpy as np
    k = np.arange(start,start+size)
    out = inarray.copy().astype(float)
    while True:
        try:
            out[k]=np.nan
            k += size + 1
        except IndexError:
            '''
            converts tail numbers to nan
            '''
            inlast_idx = inarray.size - 1
            idx = np.where(k==inlast_idx)[0]
            if idx.size>0:
                idx=idx[0]
                out[-(1+idx):]=np.nan
            return out    


def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.

    source: https://gist.github.com/vicow
    """
    from datetime import datetime,timedelta

    days = datenum % 1
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return datetime.fromordinal(int(datenum)) \
        + timedelta(days=int(days)) \
        + timedelta(hours=int(hours)) \
        + timedelta(minutes=int(minutes)) \
        + timedelta(seconds=round(seconds)) \
        - timedelta(days=366)