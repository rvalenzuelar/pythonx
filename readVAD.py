# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt
import sys

# print options
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

# open/close the file and retrieves a numpy array
data=np.loadtxt('vad.1040216150010.NOAA-D.0.0.5_PPI_v2_VV',
                dtype='float')

# command-line input arguments
cmdargs=sys.argv

# array size
asize=data.shape
rows=asize[0] # ranges
cols=asize[1] # azimuths

# define azim and veloc
azim=data[0]
veloc=data[1:]
nanvalue=-32768.
veloc[veloc==nanvalue]=np.nan

# note:
#    if find zero isodp indx then neg values
#    are defined by values < indx
#    if no zero isodop exists then all values
#    should be negative
for r in np.arange(rows-1):
    if np.any(~np.isnan(veloc[r])):
        # find index zero isodop azimuth
        idx = np.nanargmin((np.absolute(veloc[r])))
        #print veloc[r][idx]
        print idx
        
    else:
        print "ALL NAN"

NyqVel=16.09375 #m/s
thresDiff=30.0 #m/s

#velocDiff=np.absolute(np.diff(veloc))
#nancol=np.empty((rows-1,1))
#nancol[:]=np.nan
#velocDiff2=np.concatenate((velocDiff,nancol),axis=1)


ininum=int(cmdargs[1])
endnum=int(cmdargs[2])
stepnum=int(cmdargs[3])
#thisrange=range(ininum,endnum,stepnum)
#for r in thisrange:
#    plt.plot(azim,veloc[r],'o')

#plt.xlabel('azimuth[deg]')
#plt.ylabel('Radial velocity')
#plt.grid(True)
#plt.show()

#idx = np.nanargmin((np.absolute(veloc[r])))
#print veloc[r][idx]
#print veloc[r]
#print velocDiff2[r]
