'''
    Diverse utility functions

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
