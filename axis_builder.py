
"""
    Raul Valenzuela
    raul.valenzuela@colorado.edu

"""

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

plt.ioff()


def specs(rows=None, cols=None, row_ratio=None, col_ratio=None,
          figsize=None, grid=False):

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

        fig.axes.append(plt.subplot(ax))

    if grid is True:
        axes = np.array(axes).reshape((2, 3))
    else:
        axes = np.array(axes)

    return fig, axes

