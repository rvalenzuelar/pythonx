'''
    Utility functions

    Raul Valenzuela
    raul.valenzuela@colorado.edu
'''


def add_colorbar(ax, im, size=None, loc='right',label=None,
                 ticks=None, ticklabels=None, pad=None,
                 fontsize=14, invisible=False, labelpad=None):

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    divider = make_axes_locatable(ax)

    if size and loc:
        if pad is None: pad=0.05
        cax = divider.append_axes(loc, size=size, pad=pad)
    elif size:
        if pad is None: pad=0.1
        cax = divider.append_axes('right', size=size, pad=pad)
    elif loc:
        if pad is None: pad=0.05
        cax = divider.append_axes(loc, size='2%', pad=pad)
    else:
        if pad is None: pad=0.1
        cax = divider.append_axes("right", size='2%', pad=pad)

    if loc in ['top','bottom']:
        ori = 'horizontal'
        if labelpad is None: labelpad=4
    if loc == 'right':    
        ori = 'vertical'
        if labelpad is None: labelpad=10

    if ticks is None:
        cbar = plt.colorbar(im, cax=cax, orientation=ori)
    else:
        cbar = plt.colorbar(im, cax=cax, ticks=ticks,
                            orientation=ori)
    
    if invisible is True:
        ''' creates white space for correct vertical
            alignment with other subplots
        '''
        cax.remove()
    
    if loc in ['top','bottom']:
        cbar.ax.xaxis.set_ticks_position(loc)
        cbar.ax.xaxis.set_label_position(loc)
        cbar.ax.xaxis.set_tick_params(labelsize=fontsize)
        cbar.ax.set_xlabel(label,
                           fontdict=dict(size=fontsize),
                            labelpad=labelpad)      
    else:
        cbar.ax.yaxis.set_tick_params(labelsize=fontsize)
        cbar.ax.set_ylabel(label, rotation=270,
                           fontdict=dict(size=fontsize),
                            labelpad=labelpad)
    
    if ticklabels is not None:
        if isinstance(ticklabels[0],str):
            cbar.set_ticklabels(ticklabels)
        else:            
            strticklabs = list()
            for t in ticks:
                if t in ticklabels:
                    if isinstance(t,int):
                        strticklabs.append(str(t))
                    elif isinstance(t,float):
                        strticklabs.append('{}'.format(t))
                else:
                    strticklabs.append('')
            
            cbar.set_ticklabels(strticklabs)
            
    if loc == 'bottom':
        ax.xaxis.tick_top()
    
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

def format_xaxis2(ax, time_array, timelabstep=None):
    
    import numpy as np
    import pandas as pd
    from datetime import timedelta
    
    onehr = timedelta(hours=1)

    ini = time_array[0]    
    end = time_array[-1]
 
    if ini.hour not in [0,12]:
        delt=np.mod(12,ini.hour)
        if delt>5:
            delt=np.mod(24,ini.hour)
        inix = ini + onehr*delt
    else:
        inix = ini
   
    newtime = pd.date_range(inix,end,freq=timelabstep)
    ' time is start hour'
    date_fmt = '%d\n%H'
    new_xticks = np.asarray(range(len(time_array)))
    xtlabel = []
    for t in time_array:
        if pd.to_datetime(t) in newtime:
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
#	import numpy as np

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

#    return datetime.fromordinal(int(datenum))+ timedelta(days=int(days))    + timedelta(hours=int(hours))+ timedelta(minutes=int(minutes)) +timedelta(seconds=int(seconds))-timedelta(days=366)



def add_subplot_axes(ax, rect, axisbg='w'):
    
    '''
    Source:
    http://stackoverflow.com/questions/17458580/
    embedding-small-plots-inside-subplots-in-matplotlib
    
    rect=[x,y,width,heigth]    
    
    '''
    
    import matplotlib.pyplot as plt
    
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height

    inax_position = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here

    subax = fig.add_axes([x, y, width, height], axisbg=axisbg)

    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.1
    y_labelsize *= rect[3]**0.1
    
    subax.xaxis.set_tick_params(labelsize = x_labelsize)
    subax.yaxis.set_tick_params(labelsize = y_labelsize)
    
    return subax


def discrete_cmap(N, norm_range=None,base_cmap=None):
    
    ''' 
    Create an N-bin discrete colormap from the specified input map
    By Jake VanderPlas
    License: BSD-style
    source:https://gist.github.com/jakevdp/91077b0cae40f8f8244a
    '''


    import matplotlib.pyplot as plt
    import numpy as np    

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    if norm_range is None:
        bot = 0
        top = 1
    else:
        bot = norm_range[0]
        top = norm_range[1]

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(bot, top, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

def linear_reg(X,Y,const):
    
    import statsmodels.api as sm    
    import numpy as np
    
    X=np.array(X)    
    Y=np.array(Y)    
    
    bad = np.isnan(X) | np.isnan(Y)
    X=X[~bad]    
    Y=Y[~bad]    
    
    if const is True:
        X = sm.add_constant(X)
       
    model = sm.OLS(Y,X)
    result = model.fit()          
    return result
    
    







