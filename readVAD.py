# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt

# open/close the file and retrieves a numpy array
data=np.loadtxt('swp.1040216150010.NOAA-D.0.0.5_PPI_v2_V3.vad',
                dtype='float')

azim=data[0]
veloc=data[1:]
nanvalue=-32768.
veloc[veloc==nanvalue]=np.nan

index=range(40,41,1)
for i in index:
    plt.plot(azim,veloc[i])

plt.xlabel('azimuth[deg]')
plt.ylabel('Radial velocity')
plt.grid(True)
plt.show()