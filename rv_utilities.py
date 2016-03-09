'''
    A number of utility functions

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
