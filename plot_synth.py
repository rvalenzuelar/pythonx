#!//home/rvalenzuela/miniconda/bin/python

# Read netCDF file with pseudo-dual Doppler 
# synthesis and plot variables
#
# Check:
# http://matplotlib.org/examples/axes_grid/demo_axes_grid2.html
#
# Raul Valenzuela
# June, 2015

from netCDF4 import Dataset
from os import getcwd
from os.path import dirname, basename
from geographiclib.geodesic import Geodesic
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.basemap import Basemap
import sys
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def usage():

	S=	"""
		This function is copied from ~/Github/pythonx to ~/bin.
		Thus, it can be called from a directory containing 
		netCDF4 files or from any directory with syntax:
			
		$ read_cfradial_metadata.py [full path to netCDF file]
		"""
	print S

def main(filepath):
	
	# input folder
	mypath=dirname(filepath)
	myfile=basename(filepath)

	if mypath ==".":
		mypath=getcwd()
	if not myfile:
		print "Please include filename in path"
		exit()

	"""creates synthesis object"""
	S=Synthesis()

	"""assign attributes from netCDF file"""
	S.read_variables(filepath)

	"""convert to a (i,j,k) array"""
	S.adjust_dimensions()

	"""print shape of attribute arrays"""
	# print_shapes(S)

	"""print global attirutes of cedric synthesis"""
	print_global_atts(filepath)
	
	
	var="DBZ"
	plot_synth(S,var)

	# print len(S.LATG[1,:,1])
	# print len(S.LONG[:,1,1])

def print_shapes(obj):

	print "\nArray shapes:"
	print "--------------------"
	for attr, value in obj.__dict__.iteritems():	
		value=getattr(obj,attr)
		print ( "%4s = %s" % (attr, value.shape) )
	print ""

def print_global_atts(filepath):
	# open netCDF file for reading 
	synth = Dataset(filepath,'r') 
	
	nc_dims = [dim for dim in synth.dimensions]  # list of nc dimensions
	nc_vars = [var for var in synth.variables]  # list of nc variables

	print "\nGlobal attributes:"
	print "-----------------------------"
	exclude=['x','y','z','grid_type','nyquist_velocities','el']
	for var in nc_vars:
		if var.islower() and var not in exclude:
			value=synth.variables[var][:]
			if value.ndim == 0:
				print ( "%22s = %s" % (var, value) )
			elif value.ndim == 1:
				if value.dtype.char =='S':
					print ( "%22s = %s" % (var, ''.join(value)) )
				else:
					if len(value)>1:
						print ( "%22s = %s" % (var, value[:]) )
					else:
						print ( "%22s = %s" % (var, value[0]) )
			else:
				continue
	print ""

	# close netCDF  file.
	synth.close()

def swap_axes(array):

	# transform a (k,j,i) array into
	# a (i,j,k) array
	new_array=np.swapaxes(array,0,2)

	return new_array

def plot_synth(obj,var):

	# define geographic boundary
	clip=[-124.45, -122.35,37.9,39.7]

	# get array
	array=getattr(obj,var)
	zlevel=getattr(obj,'Z')

	# add figure
	fig = plt.figure(figsize=(10,15), tight_layout=True)

	dbz = [array[:,:,i+1] for i in range(6)]
	lvl = [i+1 for i in range(6)]

	grid=ImageGrid( 	fig,111,
						nrows_ncols = (3,2),
						axes_pad = 0.0,
						add_all = True,
						share_all=False,
						label_mode = "L",
						cbar_location = "top",
						cbar_mode="single")

	M = Basemap(		projection='cyl',
						llcrnrlat=clip[2],
						urcrnrlat=clip[3],
						llcrnrlon=clip[0],
						urcrnrlon=clip[1],
						resolution='i')

	# retrieve coastline
	coastline = M.coastpolygons
	lonc=coastline[1][0][15:-1]
	latc=coastline[1][1][15:-1]


	# make gridded plot
	for g,z,k in zip(grid,dbz,lvl):

		g.plot(lonc,latc, color='b')
		im = g.imshow(	z,
							interpolation='none',
							origin='lower',
							extent=clip,
							vmin=-15,
							vmax=45)
		g.grid(True)
		ztext='MSL='+str(zlevel[k])+'km'
		g.text(	0.1, 0.08,
				ztext,
				fontsize=10,
				horizontalalignment='left',
				verticalalignment='center',
				transform=g.transAxes)


 	
 	# add color bar
 	grid.cbar_axes[0].colorbar(im)

	# show figure
	plt.show()



class Synthesis(object):
	def __init__(self):
		self.X=[]
		self.Y=[]
		self.Z=[]
		self.U=[]
		self.V=[]
		self.WUP=[]
		self.WVA=[]
		self.VOR=[]
		self.DIV=[]
		self.DBZ=[]
		self.LATG=[]
		self.LONG=[]

	def read_variables(self, filepath):
		# open netCDF file for reading 
		synth = Dataset(filepath,'r') 

		var_dict={	'X':'x',
					'Y':'y',
					'Z':'z',
					'U':'F2U',
					'V':'F2V',
					'WUP':'WUPF2',
					'WVA':'WVARF2',
					'VOR':'VORT2',
					'DIV':'CONM2',
					'DBZ':'MAXDZ',
					'LATG':'LATG',
					'LONG':'LONG',
					}

		for key,value in var_dict.iteritems():
			if key in ['X','Y','Z']:
				setattr(self , key , synth.variables[value][:])
			else:
				scale = getattr(synth.variables[value],'scale_factor')
				setattr(self , key , np.squeeze(synth.variables[value][:])/scale )

		print ''.join(synth.variables['start_time'][:])

		# close netCDF  file.
		synth.close()

	def adjust_dimensions(self):
		# adjust axes to fit (X,Y,Z) dimensions
		# in 3D arrays
		for key, value in self.__dict__.iteritems():
			if key in ['X','Y','Z']:
				continue
			else:
				setattr(self,key,swap_axes(getattr(self,key)))

	def make_cart_grid(self):
		# creates a 3D cartesian grid
		self.XG,self.YG,self.ZG=np.meshgrid(self.X,self.Y,self.Z)

	def make_geo_grid(self):
		# compute horizontal grid using geodesic line
		# origin is at BBY and azimuths are in direction
		# of the cartesian axes
		lat1=0
		lon1=0
		az1=0
		line=Geodesic.WGS84.Line(lat1,lon1,az1)
		point=line.Position(grid_point)


# call main function
if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage()
		exit()
	else:
		main(sys.argv[1])