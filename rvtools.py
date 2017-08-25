'''
    Utility functions

    Raul Valenzuela
    raul.valenzuela@colorado.edu
'''


def add_colorbar(ax, im, size=None, loc='right',label=None,
                 ticks=None, ticklabels=None, pad=None,
                 fontsize=14, invisible=False, labelpad=None,
                 ticklab_inside=False, ticklab_color=None,
                 ticks_everyother=False, tick_color=None):

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
        if labelpad is None: labelpad = 4
    if loc in ['right','left']:    
        ori = 'vertical'
        if labelpad is None: labelpad = 10

    if ticks is None:
        cbar = plt.colorbar(im, cax=cax, orientation=ori)
    else:
        cbar = plt.colorbar(im, cax=cax, ticks=ticks,
                            orientation=ori)    
    cbar.ax.yaxis.tick_right()

    if invisible is True:
        ''' creates white space for correct vertical
            alignment with other subplots
        '''
        cax.remove()
    
    if loc in ['top', 'bottom']:
        cbar.ax.xaxis.set_ticks_position(loc)
        cbar.ax.xaxis.set_label_position(loc)
        if tick_color is not None:
            cbar.ax.xaxis.set_tick_params(labelsize=fontsize,
                                          color=tick_color)
        else:
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

    if ticklab_inside:
        if ori == 'horizontal':
            hgt = ax.get_position().height
            hpad = (-1.5*hgt)-5.3
            cbar.ax.xaxis.set_tick_params(pad=hpad)
            for label in cbar.ax.xaxis.get_ticklabels()[::2]:
                label.set_visible(False)
        else:
            cbar.ax.yaxis.set_tick_params(pad=-15)
            for label in cbar.ax.yaxis.get_ticklabels()[::2]:
                label.set_visible(False)

    if ticks_everyother:
        if ori == 'horizontal':
            # cbar.ax.xaxis.set_tick_params(pad=-15)
            for label in cbar.ax.xaxis.get_ticklabels()[::2]:
                label.set_visible(False)
        else:
            # cbar.ax.yaxis.set_tick_params(pad=-15)
            for label in cbar.ax.yaxis.get_ticklabels()[::2]:
                label.set_visible(False)

    if tick_color is not None:
        if ori == 'horizontal':
            cbar.ax.xaxis.set_tick_params(labelcolor=ticklab_color)
        else:
            cbar.ax.yaxis.set_tick_params(labelcolor=ticklab_color)

    return cbar

def add_floating_colorbar(fig=None, im=None, position=None,
                          loc=None, fontsize=25, label=None,
                          ticks=None, ticklabels=None,
                          clean_floating=True, labelpad=None,
                          ticklab_inside=False, ticklab_color=None,
                          tick_color=None
                          ):
    """
        Position refers to the axis position but we are interested in
        the cbar position. So, for top cbars we substract the axis hgt
        to the bottom value
    """
    lef, bot, wdt, hgt = position
    cbar_pos = [lef, bot-hgt, wdt, hgt]
    axf = fig.add_axes(cbar_pos)
    cbar = add_colorbar(axf, im, loc=loc, fontsize=fontsize,
                        label=label, labelpad=labelpad, ticks=ticks,
                        ticklabels=ticklabels,
                        ticklab_color=ticklab_color,
                        ticklab_inside=ticklab_inside,
                        tick_color=tick_color)
    if clean_floating:
        axf.remove()

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
    array of dimensions (m x n x t)

    UPDATE!!
    A faster way (this function may not be even needed)

    If S is a pandas series containing list or arrays per index:

    slist = S.tolist()
    sarray  = np.array(slist)

    '''
    
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

def fill2D_with_nans(inarray=None,start=[None,None],
                     size=[None,None]):

    outarray = inarray.copy().astype(float)

    if size[0]>0:
        ' for each column'
        for i,c in enumerate(inarray.T):
            out = fill1D_with_nans(inarray=c,
                                    start=start[0],
                                    size=size[0])
            outarray[:,i]=out

    if size[1]>0:
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

    from datetime import datetime, timedelta
    import numpy as np

    if type(datenum) == np.ndarray:
        datenum = datenum.squeeze()
        datetime_array = []
        for d in datenum:
            val = parse_datenum(d)
            datetime_array.append(val)
        return np.array(datetime_array)
    else:
        datetime_val = parse_datenum(datenum)
        return datetime_val


def parse_datenum(datenum):

    from datetime import datetime, timedelta

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
    from matplotlib.colors import LinearSegmentedColormap as lisegcmap

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

    if base_cmap in ['viridis']:
        cm = lisegcmap.from_list(cmap_name, color_list, N)
    else:
        cm = base.from_list(cmap_name, color_list, N)


    return cm

def linear_reg(X, Y, const):
    
    import statsmodels.api as sm    
    import numpy as np
    
    X = np.array(X)
    Y = np.array(Y)
    
    bad = np.isnan(X) | np.isnan(Y)
    X = X[~bad]
    Y = Y[~bad]
    
    if const is True:
        X = sm.add_constant(X)
       
    model = sm.OLS(Y,X)
    result = model.fit()          
    return result


def UO_colormap(name='UO_BrBu_10',txt_path=None,normalized=True):

    from matplotlib.colors import ListedColormap
    import numpy as np

    lines = list()
    file = open(txt_path+'/{}.txt'.format(name))
    for line in file:
        lines.append(line.rstrip())

    ''' remove header'''
    lines = lines[2:]

    rgb_list = list()
    for l in lines:
        row = l.split('    ')[-3:]
        rgb_list.append([int(r) for r in row])

    rgb_list = np.array(rgb_list)
    if normalized is True:
        rgb_list = rgb_list/256.
    cmap = ListedColormap(rgb_list,name='UO_BrBu_10', N=10)

    return cmap

def NY_colormap(file_path=None, normalized=True):

    from matplotlib.colors import ListedColormap
    import numpy as np

    # lines = list()
    # file = open(file_path)
    # for line in file:
    #     lines.append(line.rstrip())
    #
    # ''' remove header'''
    # lines = lines[2:]
    #
    # rgb_list = list()
    # for l in lines:
    #     row = l.split('    ')[-3:]
    #     rgb_list.append([int(r) for r in row])
    #
    # rgb_list = np.array(rgb_list)
    # if normalized is True:
    #     rgb_list = rgb_list/256.
    # cmap = ListedColormap(rgb_list,name='UO_BrBu_10',N=10)

    # return cmap

def get_period(year_range=list(), monthday_range=list(),freq=None):

    import pandas as pd

    md_ini = monthday_range[0]
    md_end = monthday_range[1]

    try:
        rng = [r for y in range(year_range[0], year_range[1]) for r in
               pd.date_range('{}-{}'.format(y, md_ini),
                             '{}-{}'.format(y, md_end),
                             freq=freq)
               ]
        return rng
    except ValueError:
        print 'Check if day is valid for month '






