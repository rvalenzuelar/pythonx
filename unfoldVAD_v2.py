# Read VAD files
# Raul Valenzuela
# February 2015

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf   # radial basis function module
import re                           # regular expression module


def run(filepath=''):

    data=np.loadtxt(filepath,dtype='float')

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

    # copy to new array
    oriField=np.abs(np.copy(veloc))

    # 2D interpolation
    #=============================================================================

    # creates a random sample of obs 
    x,y=np.where(~np.isnan(oriField))
    fraction=0.05
    nn=np.uint32(x.size*fraction)
    samp=np.sort(np.random.choice(np.arange(x.size),nn,replace=False))
    xsamp=x[samp]
    ysamp=y[samp]
    z=oriField[xsamp,ysamp]

    # build rbf function
    rbf=Rbf(xsamp, ysamp, z, function='linear',epsilon=1)

    # interpolate nan points
    XI,YI=np.where(np.isnan(oriField))
    ZI = rbf(XI, YI)

    # add interpolated points to field
    interpField=np.abs(np.copy(veloc))
    interpField[XI,YI]=ZI


    # zero isodop interpolation
    #=============================================================================
    
    # select grid points below a thres (i.e. along the zero isodop)    
    radialvel_thres=4.0
    yIso,xIso=np.where(interpField<radialvel_thres)

    # try to select grid points only within the isodop line
    yIso=np.asarray(yIso)
    xyIso=np.asarray(yIso)
    mask_condition=(yIso>10) & (xIso>35)
    maskyIso=np.asarray(np.where(mask_condition))
    xIsomask=np.squeeze(xIso[maskyIso])
    yIsomask=np.squeeze(yIso[maskyIso])

    # fits point to a curve
    zIso = np.polyfit(yIsomask, xIsomask, 2)
    p = np.poly1d(zIso)

    # interpolated line
    zeroisoInterp=p(np.arange(rows))


    # unfolding
    #=============================================================================
    
    NyqVel=16.09375 #m/s
    upper_zero_thres=3.0
    lower_zero_thres=-9.0
    ltolerance=3 #gate azimuth
    rtolerance=6 #gate azimuth
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
    #=============================================================================

    f1 = plt.figure(figsize=(10, 6))
    ax1=f1.add_subplot(1,3,1)
    ax=ax1.imshow(veloc,
                origin='lower',
                interpolation='none')
    ax.set_clim([-25,25])            
    # plt.colorbar(ax)
    ax1.grid(True)
    xax0,xax1=plt.xlim()
    yax0,yax1=plt.ylim()

    ax2=f1.add_subplot(1,3,2)
    ax=ax2.imshow(interpField,
                origin='lower',
                interpolation='none')
    plt.plot(zeroisoInterp,np.arange(rows), 'k')
    plt.plot(zeroisoInterp-ltolerance,np.arange(rows), 'k--')
    plt.plot(zeroisoInterp+rtolerance,np.arange(rows), 'k--')    
    # plt.plot(xIso,yIso,'ko')
    # plt.plot(xIsomask,yIsomask,'ro')
    plt.xlim([xax0,xax1])
    plt.ylim([yax0,yax1])
    ax.set_clim([-25,25])            
    # plt.colorbar(ax)
    plt.grid(True)
    

    ax3=f1.add_subplot(1,3,3)
    ax=ax3.imshow(unveloc,
                origin='lower',
                interpolation='none')
    plt.plot(zeroisoInterp,np.arange(rows), 'k')
    plt.plot(zeroisoInterp-ltolerance,np.arange(rows), 'k--')
    plt.plot(zeroisoInterp+rtolerance,np.arange(rows), 'k--')
    plt.xlim([xax0,xax1])
    plt.ylim([yax0,yax1])
    ax.set_clim([-25,25])            
    # plt.colorbar(ax)
    plt.grid(True)

    # f2 = plt.figure()
    # axh=f2.add_subplot(1,2,1)
    # axh.hist(xIso,bins=50)
    # axh=f2.add_subplot(1,2,2)
    # axh.hist(yIso,bins=50)

    # plt.show()
    
    outname= re.search('vad.(.+?).NOAA', filepath).group(1)
    # plt.savefig(outname+'_poly2.png', bbox_inches='tight')
    plt.savefig(outname+'_wRBF_poly2.png', bbox_inches='tight')
    plt.clf()
    plt.close()