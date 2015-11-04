
'''
check:
Jessica Lu
http://www.astrobetter.com/blog/2010/03/03/fourier-transforms-of-images-in-python/
'''


import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
from netCDF4 import Dataset


def main():

	# base_dir='/Users/raulv/Documents/P3/synth/'
	base_dir='/home/rvalenzuela/P3_v2/synth_prod/'

	case=7
	leg=4
	scase=str(case).zfill(2)
	sleg=str(leg).zfill(2)
	synthfile=base_dir+'c'+scase+'/leg'+sleg+'.cdf'
	U = read_synth(synthfile,'F2U')
	V = read_synth(synthfile,'F2V')

	level = 4
	Usp2D = make_2d_spectrum(U[:,:,level])
	Usp1D = make_1d_spectrum(Usp2D)

	Vsp2D = make_2d_spectrum(V[:,:,level])
	Vsp1D = make_1d_spectrum(Vsp2D)

	print U.shape
	print Usp2D.shape
	print Usp1D.shape

	# fig,ax=plt.subplots(1,2)
	# ax[0].imshow(U[:,:,level],interpolation='none')
	# ax[1].imshow(V[:,:,level],interpolation='none')
	# ax[0].set_title('U')
	# ax[1].set_title('V')
	# plt.suptitle('wind components')
	# plt.tight_layout()

	# fig,ax=plt.subplots(1,2)
	# ax[0].imshow(Usp2D,interpolation='none')
	# ax[1].imshow(Vsp2D,interpolation='none')
	# ax[0].set_title('U')
	# ax[1].set_title('V')

	fig,ax=plt.subplots(1,2)
	ax[0].semilogy(Usp1D)
	ax[1].semilogy(Vsp1D)
	ax[0].set_title('U')
	ax[1].set_title('V')
	ax[0].set_ylim([1e10,1e16])
	ax[1].set_ylim([1e10,1e16])
	plt.suptitle('power spectrum case '+scase+' leg '+sleg)
	
	plt.show(block=False)
	


def make_2d_spectrum(array):

	''' Take the fourier transform of the image. '''
	F1 = fftpack.fft2(array)

	''' Now shift the quadrants around so that low spatial frequencies are in
	 the center of the 2D fourier transformed image.'''
	F2 = fftpack.fftshift(F1)

	''' Calculate a 2D power spectrum '''
	psd2D = np.abs( F2 )**2

	return psd2D

def make_1d_spectrum(spectrum2D):

	''' Calculate the azimuthally averaged 1D power spectrum '''
	psd1D = azimuthalAverage(spectrum2D)

	return psd1D

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

def read_synth(synthfile, var):

	# open netCDF file for reading 
	synth = Dataset(synthfile,'r') 

	# assing values from synthesis to instance attirbutes
	if var in ['x','y','z']:
		array = synth.variables[var][:]
	else:
		scale = getattr(synth.variables[var],'scale_factor')
		array = np.squeeze(synth.variables[var][:])/scale 
		array = np.swapaxes(array,0,2)

	# close netCDF  file.
	synth.close()

	return array    

def read_field():
	
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

main()    