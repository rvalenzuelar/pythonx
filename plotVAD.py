# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold='nan')

# open/close the file and retrieves a numpy array

vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
# vadfile='vad.1040216151826.NOAA-D.0.0.5_PPI_v64_V3'
# vadfile='vad.1040216153642.NOAA-D.0.0.5_PPI_v119_V3'
# vadfile='vad.1040216173830.NOAA-D.0.0.5_PPI_v124_V3'
# vadfile='vad.1040216185745.NOAA-D.0.0.5_PPI_v187_V3'
# vadfile='vad.1040216171410.NOAA-D.0.0.5_PPI_v46_V3'

#vadfile='vad.1040216164949.NOAA-D.0.0.5_PPI_v161_V3'

data=np.loadtxt(vadfile,dtype='float')

# array size
asize=data.shape
rows=asize[0] # ranges
cols=asize[1] # azimuths


# define azim and veloc
azim=data[0]
veloc=data[1:]
nanvalue=-32768.

veloc[veloc==nanvalue]=np.nan
unveloc=np.copy(veloc)



plt.figure

ax=plt.imshow(veloc,
            origin='lower',
            interpolation='none')
ax.set_clim([-25,25])            
plt.colorbar(ax)
plt.grid(True)


plt.show()

