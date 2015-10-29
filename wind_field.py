
'''
check:
Jessica Lu
http://www.astrobetter.com/blog/2010/03/03/fourier-transforms-of-images-in-python/
'''


import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack


def main():
	x,y = np.meshgrid(range(-25,25),range(-25,25))


	u = np.sin(0.9*x)
	v = np.cos(0.1*y)

	''' Take the fourier transform of the image. '''
	F1 = fftpack.fft2(u)

	''' Now shift the quadrants around so that low spatial frequencies are in
	 the center of the 2D fourier transformed image.'''
	F2 = fftpack.fftshift( F1 )

	''' Calculate a 2D power spectrum '''
	psd2D = np.abs( F2 )**2

	''' Calculate the azimuthally averaged 1D power spectrum '''
	psd1D = azimuthalAverage(psd2D)


	fig,ax=plt.subplots()
	ax.imshow(u)
	plt.axis('equal')

	fig,ax=plt.subplots()
	ax.imshow(psd2D)
	plt.axis('equal')

	fig,ax=plt.subplots()
	ax.semilogy(psd1D)
	# plt.axis('equal')

	fig,ax=plt.subplots()
	ax.quiver(u,v,scale=20)
	plt.axis('equal')

	plt.show()

def azimuthalAverage(image, center=None):
    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is 
             None, which then uses the center of the image (including 
             fracitonal pixels).
    
    Jessica Lu
    """
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (y.max()-y.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin
    
    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof

main()    