
'''
	Analysis of wind field from P3 synthesis 
	Raul Valenzuela
	November, 2015

	For 2D spectrum plotting check Jessica Lu:
	http://www.astrobetter.com/blog/2010/03/03/fourier-transforms-of-images-in-python/
'''


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import seaborn as sns

from scipy import fftpack
from netCDF4 import Dataset
from mpl_toolkits.axes_grid1 import make_axes_locatable

base_dir='/home/rvalenzuela/P3_v2/synth_prod/'

def main():

	# base_dir='/Users/raulv/Documents/P3/synth/'

	case=7
	leg=5
	scase=str(case).zfill(2)
	sleg=str(leg).zfill(2)
	synthfile=base_dir+'c'+scase+'/leg'+sleg+'.cdf'

	U = read_synth(synthfile,'F2U')
	V = read_synth(synthfile,'F2V')
	Z = read_synth(synthfile,'z')

	level = 4
	# plot_spectrum(U,V,Z,level,scase,sleg)
	# plot_fields(U,V,Z,level,scase,sleg)
	

	synth={3:[1,3,5,12,14,16], 7:[3,4,5,6]}
	plot_profile_variance_wind(synth)
	plot_profile_variance_dbz(synth)
	# plot_profile_valid_gates(synth,'wind')
	# plot_profile_valid_gates(synth,'dbz')

			
	plt.show(block=False)


def plot_profile_variance_wind(synth):

	fig,ax=plt.subplots()
	colors=get_colors(synth)
	c=0	
	for key,value in synth.iteritems():
		for v in value:
			scase=str(key).zfill(2)
			sleg=str(v).zfill(2)
			synthfile=base_dir+'c'+scase+'/leg'+sleg+'.cdf'
			U = read_synth(synthfile,'F2U')
			V = read_synth(synthfile,'F2V')
			Z = read_synth(synthfile,'z')
			x=[]
			y=[]
			for n,z in enumerate(Z[1:15]):
				u=U[:,:,n+1]
				v=V[:,:,n+1]
				wdir = (np.arctan2(u,v)*180/np.pi)+180.
				x.append(np.nanvar(wdir))
				y.append(z)
			label='Case: '+scase+' Leg: '+sleg
			ax.plot(x,y,'-',label=label,color=colors[c])
			ax.set_ylim([0,4])
			ax.set_xlabel('Wind direction variance [deg^2]')
			ax.set_ylabel('Altitude MSL [km]')
			c+=1
	plt.suptitle('Spatial variance at P3 synth levels ')			
	plt.draw()
	plt.legend()

def plot_profile_variance_dbz(synth):

	fig,ax=plt.subplots()
	colors=get_colors(synth)
	c=0	
	for key,value in synth.iteritems():
		for v in value:
			scase=str(key).zfill(2)
			sleg=str(v).zfill(2)
			synthfile=base_dir+'c'+scase+'/leg'+sleg+'.cdf'
			DBZ = read_synth(synthfile,'MAXDZ')
			Z = read_synth(synthfile,'z')
			x=[]
			y=[]
			for n,z in enumerate(Z[1:15]):
				dbz=DBZ[:,:,n+1]
				x.append(np.nanvar(dbz))
				# zz=10**(dbz/10.)
				# x.append(np.nanvar(zz)) # similar than dbz but in linear scale
				y.append(z)

			label='Case: '+scase+' Leg: '+sleg
			ax.plot(x,y,'-',label=label,color=colors[c])
			ax.set_ylim([0,4])
			ax.set_xlabel('Reflectivity variance [dBZ^2]')
			ax.set_ylabel('Altitude MSL [km]')
			c+=1
	plt.suptitle('Spatial variance at P3 synth levels ')			
	plt.draw()
	plt.legend()

def plot_profile_valid_gates(synth,field):

	fig,ax=plt.subplots()

	if field=='wind':
		synthvar='F2U' # U and V has same number of valid gates
	elif field=='dbz':
		synthvar='MAXDZ'

	colors=get_colors(synth)
	c=0
	for key,value in synth.iteritems():
		for v in value:
			scase=str(key).zfill(2)
			sleg=str(v).zfill(2)
			synthfile=base_dir+'c'+scase+'/leg'+sleg+'.cdf'
			SVAR = read_synth(synthfile,synthvar)
			Z = read_synth(synthfile,'z')
			x=[]
			y=[]
			for n,z in enumerate(Z[1:15]):
				svar=SVAR[:,:,n+1]
				x.append(svar.count())
				y.append(z)
			label='Case: '+scase+' Leg: '+sleg
			ax.plot(x,y,'-o',label=label,color=colors[c])
			ax.set_ylim([0,4])
			ax.set_xlabel('Count')
			ax.set_ylabel('Altitude MSL [km]')
			c+=1
	plt.suptitle('Valid gates in '+field)
	plt.draw()
	plt.legend()

def get_colors(synth):


	p=['Blues','Reds','Greens']
	# p=[0,1,2]
	colors=[]
	for n,k in enumerate(synth):
		cs= sns.color_palette(p[n],20,desat=.5)
		for x,v in enumerate(synth[k]):
			colors.append(cs[(x*2)+5])
	return colors

def plot_fields(U,V,Z,level,scase,sleg):

	u=U[:,:,level].T
	v=V[:,:,level].T
	wdir = (np.arctan2(u,v)*180/np.pi)+180.

	u_var=np.nanvar(u)
	v_var=np.nanvar(v)
	wdir_var=np.nanvar(wdir)
	var=[u_var, v_var, wdir_var]

	ax=[]
	im=[]
	fig = plt.figure(figsize=(15,5))
	gs = gridspec.GridSpec(1, 3)
	gs.update(wspace=0.05)
	ax.append(plt.subplot(gs[0]))
	ax.append(plt.subplot(gs[1],sharey=ax[0]))
	ax.append(plt.subplot(gs[2],sharey=ax[0]))
	im.append(ax[0].imshow(u,interpolation='none',origin='lower',aspect=1,vmin=-7,vmax=7,cmap='RdBu'))
	im.append(ax[1].imshow(v,interpolation='none',origin='lower',aspect=1,cmap='Blues'))
	im.append(ax[2].imshow(wdir,interpolation='none',origin='lower',aspect=1,vmin=160,vmax=220,cmap='PRGn'))

	imstr=['U-wind','V-wind','WDIR']
	for n,x in enumerate(ax):
		divider = make_axes_locatable(x)
		cax = divider.append_axes("top", size="2%", pad=0.05)
		cbar = plt.colorbar(im[n], cax=cax, orientation='horizontal')
		cbar.ax.xaxis.set_ticks_position('top')
		cbar.ax.xaxis.set_label_position('top')
		x.text(10,120,imstr[n],weight='bold')
		x.text(10,10,'Variance = {:3.2f}'.format(var[n]),weight='bold')

	alt='{:3.2f}'.format(Z[level])
	plt.suptitle('P3 Synthesis case '+scase+' leg '+sleg+' altitude: '+alt+'km MSL')
	plt.draw()
	
def plot_spectrum(U,V,Z,level,scase,sleg):

	Usp2D = make_2d_spectrum(U[:,:,level])
	Usp1D = make_1d_spectrum(Usp2D)

	Vsp2D = make_2d_spectrum(V[:,:,level])
	Vsp1D = make_1d_spectrum(Vsp2D)

	SPD=np.sqrt(U**2+V**2)
	SPDsp2D = make_2d_spectrum(SPD[:,:,level])
	SPDsp1D = make_1d_spectrum(SPDsp2D)

	fig,ax=plt.subplots(1,3,sharey=True)
	ax[0].semilogy(Usp1D)
	ax[1].semilogy(Vsp1D)
	ax[2].semilogy(Vsp1D)
	ax[0].set_title('U')
	ax[1].set_title('V')
	ax[2].set_title('SPD')
	ax[0].set_ylim([1e10,1e16])
	ax[1].set_ylim([1e10,1e16])
	ax[2].set_ylim([1e10,1e16])
	alt='{:3.2f}'.format(Z[level])
	plt.suptitle('Power spectrum case '+scase+' leg '+sleg+' altitude: '+alt+'km MSL')
	plt.draw()

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