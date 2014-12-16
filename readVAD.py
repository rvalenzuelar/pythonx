# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt

# loadtxt open/close the file and retrieves a numpy array
data=np.loadtxt('swp.1040216150010.NOAA-D.0.0.5_PPI_v2_V3.vad',
                dtype='float')

azim=data[0]
veloc=data[1:]

veloc[veloc==-32768.]=np.nan

plt.plot(azim,veloc[20])
plt.xlabel('azimuth[deg]')
plt.ylabel('Radial velocity')
plt.grid(True)
plt.show()