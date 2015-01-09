# Read VAD files
# Raul Valenzuela
# December 2014

import numpy as np
import matplotlib.pyplot as plt
import sys

# print options
np.set_printoptions(precision=1)
np.set_printoptions(suppress=True)

# open/close the file and retrieves a numpy array

vadfile='vad.1040216150010.NOAA-D.0.0.5_PPI_v2_V3'
#vadfile='vad.1040216164949.NOAA-D.0.0.5_PPI_v161_V3'
data=np.loadtxt(vadfile,dtype='float')

# command-line input arguments
cmdargs=sys.argv
iniring=int(cmdargs[1])
endring=int(cmdargs[2])
stepring=int(cmdargs[3])
lowslice=int(cmdargs[4])
uppslice=int(cmdargs[5])

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

NyqVel=16.09375 #m/s
thresDiff=30.0 #m/s

# note:
#   * if find zero isodop indx then neg values
#     are defined by values < indx
#   * if no zero isodop exists in a given ring
#     then look for isodop indx in previous rins
#     as a refernece
#   * if no zero isodop exists in a given sweep
#     then all values should be negative (?)

# for each ring
for r in np.arange(rows-1):
    # if ring has non nan values
    if np.any(~np.isnan(veloc[r])):
        # find index of velo closest to zero isodop
        # assumes that the lowest abs(velo) corresponds
        # to the zero isodop
        idx = np.nanargmin((np.absolute(veloc[r])))
      
        # if idx is outside of the cols' middle third then it is
        # probable that it is not the zero isodop index
        lowlim=np.round(cols/3)
        upplim=np.round(2*cols/3)
        #print lowlim,upplim, idx
        #while status==False:
        if idx<lowlim or idx>upplim:
            #way 1
            #idx = np.nanargmin((np.absolute(veloc[r-1])))

            #way 2
            #x=np.argsort(np.absolute(veloc[r]))
            #idx=x[1]
            
            #way 3
            idx = np.nanargmin((np.absolute(veloc[r,lowlim:upplim])))
            idx = idx+lowlim
        upper_zero_thres=2.5
        lower_zero_thres=-2.5
        for a in np.arange(cols-1):
            if a<idx and veloc[r,a]>upper_zero_thres:             
                unveloc[r,a]=veloc[r,a]-2*NyqVel
            if a>idx and veloc[r,a]<lower_zero_thres:             
                unveloc[r,a]=veloc[r,a]+2*NyqVel
        if r==iniring:
            print veloc[r,0:lowlim]
            print veloc[r,lowlim:upplim]
            print veloc[r,upplim:]            
            print veloc[r,idx], r 
            print lowlim, idx, upplim       
            #print unveloc[r,0:lowlim]

    else:
        print "ALL NAN"


#thisrange=range(iniring,endring,stepring)
#plt.figure(1)
#for r in thisrange:
#    #plt.scatter(azim,unveloc[r],c='red',s=100)
#    #plt.scatter(azim,veloc[r],c='blue',s=25)
#    plt.plot(azim,unveloc[r])
#
#plt.xlabel('azimuth[deg]')
#plt.ylabel('Radial velocity')
#plt.grid(True)


asp_op='1'
int_op='none'

plt.subplot(2,1,1)
plt.imshow(veloc[lowslice:uppslice,:],
            origin='lower',
            aspect=asp_op,
            interpolation=int_op)
plt.subplot(2,1,2)
plt.imshow(unveloc[lowslice:uppslice,:],
            origin='lower',
            aspect=asp_op,
            interpolation=int_op)

#plt.imshow(unveloc,
#            origin='lower',
#            interpolation=int_op)

plt.show()

