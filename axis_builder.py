
"""
    Raul Valenzuela
    raul.valenzuela@colorado.edu

"""
import matplotlib.pyplot as plt

plt.ioff()

import matplotlib.gridspec as gridspec
import numpy as np
import string



def specs(rows=None, cols=None, row_ratio=None, col_ratio=None,
          figsize=None, return_grid=False, name_loc='upper-left',
          hide_labels_in=None, hide_xlabels_in=None,
          hide_ylabels_in=None,
          hspace=None, wspace=None):

    if figsize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(rows, cols,
                           width_ratios=col_ratio,
                           height_ratios=row_ratio
                           )

    axes = list()
    for ax in gs:
        axes.append(plt.subplot(ax))
    axes = np.array(axes)

    if isinstance(name_loc,str):
        if name_loc == 'upper-left':
            loc_coord = (0.05, 0.90)
        elif name_loc == 'upper-right':
            loc_coord = (0.90, 0.90)
    else:
        loc_coord = name_loc

    pname = iter(list(string.ascii_lowercase)[:rows*cols])
    for p, ax, in zip(pname, axes):
        transf = ax.transAxes
        ax.text(loc_coord[0], loc_coord[1], '({})'.format(p),
                fontsize=15,
                weight='bold',
                transform=transf,
                color=(0.3, 0.3, 0.3))

    if hide_labels_in is not None:
        for h in hide_labels_in:
            axes[h].set_xticklabels('')
            axes[h].set_yticklabels('')

    if hide_xlabels_in is not None:
        for h in hide_xlabels_in:
            axes[h].set_xticklabels('')

    if hide_ylabels_in is not None:
        for h in hide_ylabels_in:
            axes[h].set_yticklabels('')

    if return_grid is True:
        axes = axes.reshape((rows, cols))

    if hspace is not None:
        plt.subplots_adjust(hspace=hspace)

    if wspace is not None:
        plt.subplots_adjust(wspace=wspace)

    return fig, axes

