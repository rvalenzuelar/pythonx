# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt
import sys
from pandas import Series
import pandas as pd
from scipy import ndimage
import cv2
from PIL import Image
from skimage import img_as_ubyte


def scale_linear(rawarray,low=-1.0,high=1.0):
    mins = np.nanmin(rawarray)
    maxs = np.nanmax(rawarray)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawarray)) / rng)

def find_closest(A, target):
    #A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx

# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)
np.set_printoptions(threshold='nan')

# open/close the file and retrieves a numpy array

#vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
#vadfile='vad.1040216151826.NOAA-D.0.0.5_PPI_v64_V3'
#vadfile='vad.1040216153642.NOAA-D.0.0.5_PPI_v119_V3'
#vadfile='vad.1040216173830.NOAA-D.0.0.5_PPI_v124_V3'
#vadfile='vad.1040216185745.NOAA-D.0.0.5_PPI_v187_V3'
vadfile='vad.1040216171410.NOAA-D.0.0.5_PPI_v46_V3'

#vadfile='vad.1040216164949.NOAA-D.0.0.5_PPI_v161_V3'
data=np.loadtxt(vadfile,dtype='float')

# array size
asize=data.shape
rows=asize[0] # ranges
cols=asize[1] # azimuths

# command-line input arguments
try:
    cmdargs=sys.argv
    iniring=int(cmdargs[1])
    endring=int(cmdargs[2])
    stepring=int(cmdargs[3])
    lowslice=int(cmdargs[4])
    uppslice=int(cmdargs[5])        
except IndexError:
    # default arguments
    iniring=1
    endring=rows
    stepring=1
    lowslice=0
    uppslice=rows

# define azim and veloc
azim=data[0]
veloc=data[1:]
nanvalue=-32768.

veloc[veloc==nanvalue]=np.nan
unveloc=np.copy(veloc)

# ------------------------------------------------------------------
# scale velocity
# velscaled=scale_linear(veloc,-1,1)
# convert to a 8-bit image
# img=img_as_ubyte(velscaled, force_copy=False)

velocsub=np.abs(np.copy(veloc[10:100,100:150]))
velocsub[np.isnan(velocsub)]=0.0
velscaled=scale_linear(velocsub,-1,1)

img=img_as_ubyte(velscaled, force_copy=False)
# create mask for inpaint
# img_mask=np.zeros(veloc.shape,np.uint8)
img_mask=np.zeros(velocsub.shape,np.uint8)
img_mask[~np.isnan(veloc[10:100,100:150])]=0
img_mask[np.isnan(veloc[10:100,100:150])]=1
#interpolate with inpaint
velocinp = cv2.inpaint(img,img_mask, 5, cv2.INPAINT_NS)

# velocinp2=scale_linear(np.float32(velocinp),-16,16)

# print velocinp[10,:]
# for g in np.arange(rows-1):
#     itemindex = find_closest(velocinp[g,:],0)
#     print itemindex
# ------------------------------------------------------------------

NyqVel=16.09375 #m/s
thresDiff=30.0 #m/s


# note:
#   * assume negative values to the left of a zero 
#     isodop indx
#   * if no zero isodop exists in a given ring
#     then look for isodop indx in previous ring
#     as a reference
#   * if no zero isodop exists in a given sweep
#     then all values should be negative (?)

# for each ring
for r in np.arange(rows-1):
    # make sure ring has non-nan values
    if np.any(~np.isnan(veloc[r])):
        # find index of velocity closest to zero isodop
        # assumes that the lowest abs(velo) corresponds
        # to the zero isodop
        idx = np.nanargmin((np.absolute(veloc[r])))

        idxlowlim=np.round(cols/3)
        #idxupplim=np.round(2*cols/3)
        
        #print r
                
        # if idx exists within the first third of the ring 
        # then it is probable that it is not the zero isodop 
        # index given the kinematic structure of the data
        # (e.g. zero isodop moving to right)
        if idx<idxlowlim:           
        #if idx<110:           
            # look for the index in the 2/3 to the right
            try:
                idx = np.nanargmin((np.absolute(veloc[r,idxlowlim:])))                
                #idx = np.nanargmin((np.absolute(veloc[r,100:])))
                idx = idx+idxlowlim
            except ValueError:
                idx=160            
        #print idx
        # define a threshold to bound the zero isodop
        upper_zero_thres=3.0
        lower_zero_thres=-3.0
        # loop for unfolding
        for a in np.arange(cols-1):
            if a<idx and veloc[r,a]>upper_zero_thres:             
                unveloc[r,a]=veloc[r,a]-2*NyqVel
            if a>idx and veloc[r,a]<lower_zero_thres:             
                unveloc[r,a]=veloc[r,a]+2*NyqVel
        if r==203:
            print veloc[r,:]          
            print veloc[r,idx], r, idx 
            print unveloc[r,:]
    else:
        print "ALL NAN"

#thisrange=range(iniring,endring,stepring)
#plt.figure(1)
#for r in thisrange:
#    #plt.scatter(azim,unveloc[r],c='red',s=100)
#    #plt.scatter(azim,veloc[r],c='blue',s=25)
#    plt.plot(azim,unveloc[r])
#plt.xlabel('azimuth[deg]')
#plt.ylabel('Radial velocity')
#plt.grid(True)

#-----------------------------------------------------
#pickazim=78 # column
#beam=Series(unveloc[:,pickazim]) # <-- pandas object
#beam0=Series(veloc[:,pickazim]) # <-- pandas object
#
##print beam.describe()
##beam_nonan=beam.dropna()
#
#mov_std=pd.rolling_std(beam,20,min_periods=2)
##mov_std=pd.rolling_std(beam,5)
#
##print beam0.values
##print beam.values
##print mov_std.values
#
#mask=(mov_std>5) & (beam>0)
#
#beam[mask]=beam[mask]-2*NyqVel
##print beam.values
#-----------------------------------------------------

# second pass for unfolding based on moving average
# along the beam
for az in np.arange(cols-1):
    # beam at ranges slightly appart from
    # the coast
    beam=Series(unveloc[10:,az]) 
    window=20
    mov_std=pd.rolling_std(beam,window,min_periods=10)    
    mask=(mov_std>8) & (beam>0)
    beam[mask]=beam[mask]-2*NyqVel
    unveloc[10:,az]=beam

# edge detection
sx = ndimage.sobel(unveloc, axis=0, mode='constant')
sy = ndimage.sobel(unveloc, axis=1, mode='constant')
sob = np.hypot(sx, sy)
print np.nanmean(sob)


# make plots
asp_op='1'
int_op='none'

plt.figure(1)
plt.subplot(2,1,1)
ax=plt.imshow(veloc[lowslice:uppslice,:],
            origin='lower',
            interpolation=int_op)
ax.set_clim([-25,25])            
plt.colorbar(ax)
plt.grid(True)

plt.subplot(2,1,2)
ax=plt.imshow(unveloc[lowslice:uppslice,:],
            origin='lower',
            interpolation=int_op)
ax.set_clim([-25,25])            
plt.colorbar(ax)
plt.grid(True)
plt.show()

#plt.figure(2)
#plt.plot(np.arange(rows-1),beam,'ro')
#plt.show()
#
#plt.figure(3)
#beam_nonan.plot(kind='hist',bins=50)

plt.figure(4)
plt.subplot(1,2,1)
plt.imshow(unveloc,
            origin='lower',
            interpolation=int_op)
plt.subplot(1,2,2)
ax=plt.imshow(sob,
            origin='lower',
            interpolation=int_op)
plt.colorbar(ax)            
plt.show()

plt.figure(5)
plt.subplot(1,3,1)
ax=plt.imshow(np.abs(veloc[10:100,100:150]),
            origin='lower',
            interpolation=int_op)          
plt.clim(0, 6)
plt.colorbar(ax) 
plt.subplot(1,3,2)
plt.imshow(img_mask,
            origin='lower',
            interpolation=int_op)
plt.subplot(1,3,3)
ax=plt.imshow(velocinp,
            origin='lower',
            interpolation=int_op)
plt.clim(0, 120)
plt.colorbar(ax) 
plt.show()

print velocinp