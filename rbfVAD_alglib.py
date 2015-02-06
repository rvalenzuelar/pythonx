# Interpolate 2D array using RBF in alglib
# Raul Valenzuela
# February 2015

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import xalglib as alg


# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold='nan')

#vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
#vadfile='vad.1040216151826.NOAA-D.0.0.5_PPI_v64_V3'
#vadfile='vad.1040216153642.NOAA-D.0.0.5_PPI_v119_V3'
#vadfile='vad.1040216173830.NOAA-D.0.0.5_PPI_v124_V3'
#vadfile='vad.1040216185745.NOAA-D.0.0.5_PPI_v187_V3'
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
xsub=slice(80,110)
ysub=slice(80,110)
velocsub=np.abs(np.copy(veloc[xsub,ysub]))

# make vectors
x,y=np.where(~np.isnan(velocsub))
z=velocsub[x,y]

# create data array (need transpose)
xyz=np.array([x,y,z],np.float).T
xyz0=xyz.tolist()

# creates 2D model (2) with scalar 
# function values (1)
model = alg.rbfcreate(2, 1)

# include obs into the model
alg.rbfsetpoints(model, xyz0)

# sets the model
radius=5.0
nlayers=3
lamb=1.0e-3
alg.rbfsetalgomultilayer(model,radius,nlayers,lamb)

# build the model and return a report
rep = alg.rbfbuildmodel(model)

xg=np.arange(velocsub.shape[0],dtype='float32')
yg=np.arange(velocsub.shape[1],dtype='float32')
XG, YG = np.meshgrid(xg, yg)

xi=np.reshape(XG,np.size(XG))
yi=np.reshape(YG,np.size(YG))
x0=xi.tolist()
x1=yi.tolist()
zi=alg.rbfgridcalc2(model,x0,xi.size,x1,yi.size)



plt.figure
plt.subplot(1,2,1)
ax=plt.imshow(velocsub,
            origin='lower',
            interpolation='none')
ax.set_clim([0,25])
plt.grid(True)
plt.subplot(1,2,2)
ax=plt.imshow(zi,
            origin='lower',
            interpolation='none')
ax.set_clim([0,25])
plt.grid(True)
plt.show()