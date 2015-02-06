# Interpolate 2D array
# Raul Valenzuela
# February 2015
# 
# Uses a small region of the VAD to 
# apply the rbf
# 



import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import Rbf

# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold='nan')

# vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
# vadfile='vad.1040216151826.NOAA-D.0.0.5_PPI_v64_V3'
# vadfile='vad.1040216153642.NOAA-D.0.0.5_PPI_v119_V3'
# vadfile='vad.1040216173830.NOAA-D.0.0.5_PPI_v124_V3'
# vadfile='vad.1040216185745.NOAA-D.0.0.5_PPI_v187_V3'
vadfile='vad.1040216171410.NOAA-D.0.0.5_PPI_v46_V3'

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
rangeInterp=p(np.arange(rows))

plt.figure

plt.subplot(1,2,1)
ax1=plt.imshow(np.abs(veloc[xsub,ysub]),
            origin='lower',
            interpolation='none')
ax1.set_clim([0,25])
xax0,xax1=plt.xlim()
yax0,yax1=plt.ylim()
# plt.grid(True)

plt.subplot(1,2,2)
ax2=plt.imshow(interpField,
            origin='lower',
            interpolation='none')
ax2.set_clim([0,25])
plt.plot(xIso, yIso, 'ro')
plt.plot(rangeInterp,np.arange(rows), 'w')
plt.xlim([xax0,xax1])
plt.ylim([yax0,yax1])

plt.show()

