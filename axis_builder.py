
"""
    Raul Valenzuela
    raul.valenzuela@colorado.edu

"""
import matplotlib.pyplot as plt

# plt.ioff()

import matplotlib.gridspec as gridspec
import numpy as np
import string



def specs(rows=None, cols=None, id_panels=True,
          row_ratio=None, col_ratio=None,
          figsize=None, return_grid=False, name_loc='upper-left',
          hide_labels_in=None, hide_xlabels_in=None,
          hide_ylabels_in=None, show_grid=False,
          hspace=None, wspace=None, left=None, right=None,
          top=None, bottom=None, sharex=False, sharey=False):

    if figsize is None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(rows, cols,
                           width_ratios=col_ratio,
                           height_ratios=row_ratio,
                           )

    axes = list()
    for n, g in enumerate(gs):
        if n == 0:
            ax0 = fig.add_subplot(g)
            axes.append(ax0)
        else:
            ''' not working, need to check why'''
            if sharex and sharey:
                ax = fig.add_subplot(g,
                                    sharex=ax0,
                                    sharey=ax0)
            elif sharex:
                ax = fig.add_subplot(g, sharex=ax0)
            elif sharey:
                ax = fig.add_subplot(g, sharey=ax0)
            else:
                ax = fig.add_subplot(g)
            axes.append(ax)

    axes = np.array(axes)

    if id_panels:
        if isinstance(name_loc,str):
            if name_loc == 'upper-left':
                loc_coord = (0.05, 0.90)
            elif name_loc == 'upper-right':
                loc_coord = (0.85, 0.90)
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

    if show_grid:
        for ax in axes:
            ax.grid(True)

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

    if left is not None:
        plt.subplots_adjust(left=left)

    if right is not None:
        plt.subplots_adjust(right=right)

    if top is not None:
        plt.subplots_adjust(top=top)

    if bottom is not None:
        plt.subplots_adjust(bottom=bottom)

    return fig, axes

