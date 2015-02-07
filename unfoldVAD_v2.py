# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf



# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold='nan')

# open/close the file and retrieves a numpy array

# vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
# vadfile='vad.1040216151826.NOAA-D.0.0.5_PPI_v64_V3'
# vadfile='vad.1040216153642.NOAA-D.0.0.5_PPI_v119_V3'
# vadfile='vad.1040216173830.NOAA-D.0.0.5_PPI_v124_V3'
# vadfile='vad.1040216185745.NOAA-D.0.0.5_PPI_v187_V3'
vadfile='vad.1040216171410.NOAA-D.0.0.5_PPI_v46_V3'

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

# subset array
# xsub=slice(10,100)
xsub=slice(10,259)
ysub=slice(15,180)

# copy field
interpField=np.abs(np.copy(veloc[xsub,ysub]))

# creates a random sample of obs 
x,y=np.where(~np.isnan(interpField))
fraction=0.05
nn=np.uint32(x.size*fraction)
samp=np.sort(np.random.choice(np.arange(x.size),nn,replace=False))
xsamp=x[samp]
ysamp=y[samp]
z=interpField[xsamp,ysamp]

# build rbf function
rbf=Rbf(xsamp, ysamp, z, function='linear',epsilon=1)

# interpolate nan points
XI,YI=np.where(np.isnan(interpField))
ZI = rbf(XI, YI)

# add interpolated points to field
interpField[XI,YI]=ZI

# coordinates of zero isodop
yIso,xIso=np.where(interpField<1.0)

# fits point to a curve
zIso = np.polyfit(yIso, xIso, 2)
p = np.poly1d(zIso)
zeroisoInterp=p(np.arange(rows))

# unfolding
NyqVel=16.09375 #m/s
upper_zero_thres=3.0
lower_zero_thres=-10.0
ltolerance=3 #gates
rtolerance=6 #gates
# for each ring
for r in np.arange(rows-1):
    # make sure ring has non-nan values
    if np.any(~np.isnan(veloc[r])):
        idx=np.uint32(zeroisoInterp[r])
        # loop for unfolding
        for a in np.arange(cols-1):
            if a<idx-ltolerance and veloc[r,a]>upper_zero_thres:
                unveloc[r,a]=veloc[r,a]-2*NyqVel
            if a>idx+rtolerance and veloc[r,a]<lower_zero_thres:
                unveloc[r,a]=veloc[r,a]+2*NyqVel
    else:
        print "ALL NAN"



# make plots
asp_op='1'
int_op='none'

plt.figure(1)
plt.subplot(1,2,1)
ax=plt.imshow(veloc,
            origin='lower',
            interpolation=int_op)
ax.set_clim([-25,25])            
# plt.colorbar(ax)
plt.grid(True)
xax0,xax1=plt.xlim()
yax0,yax1=plt.ylim()

plt.subplot(1,2,2)
ax=plt.imshow(unveloc,
            origin='lower',
            interpolation=int_op)
plt.plot(zeroisoInterp,np.arange(rows), 'k')
plt.plot(zeroisoInterp-ltolerance,np.arange(rows), 'k--')
plt.plot(zeroisoInterp+rtolerance,np.arange(rows), 'k--')

plt.xlim([xax0,xax1])
plt.ylim([yax0,yax1])
ax.set_clim([-25,25])            
# plt.colorbar(ax)
plt.grid(True)
plt.show()