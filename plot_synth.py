#!//home/rvalenzuela/miniconda/bin/python

# Read netCDF file with pseudo-dual Doppler 
# synthesis and plot variables
#
# Check:
# http://matplotlib.org/examples/axes_grid/demo_axes_grid2.html
#
# Raul Valenzuela
# June, 2015

from os import getcwd
from os.path import dirname, basename
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.basemap import Basemap
import sys
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import AircraftAnalysis as aa 

def usage():

	desc=	"""
		This function is copied from ~/Github/pythonx to ~/bin.
		Thus, it can be called from a directory containing 
		netCDF4 files or from any directory with syntax:
			
		$ read_cfradial_metadata.py [path to netCDF file]
		"""
	print desc

def main(filepath, stdfile):
	
	# base directory
	basedirectory = "/home/rvalenzuela/P3_v2/synth_test/"
	stdtapedir = "/home/rvalenzuela/Github/correct_dorade_metadata/"

	# input folder
	mypath=dirname(filepath)
	myfile=basename(filepath)

	
	if mypath ==".":
		mypath=getcwd()
		filepath=mypath+filepath
	else:
		mypath=basedirectory
		filepath=mypath+filepath

	if not myfile:
		print "Please include filename in path"
		exit()

	""" creates a synthesis """
	S=aa.Synthesis(filepath)

	""" creates a std tape """
	T=aa.Stdtape(stdtapedir+stdfile)

	""" creates a flightpath """
	F=T.Flightpath(S.start, S.end)

	""" print shape of attribute arrays """
	# S.print_shapes()

	""" print global attirutes of cedric synthesis """
	# S.print_global_atts()
	

	""" print synthesis time """
	print "\nSynthesis start time :%s" % S.start
	print "Synthesis end time :%s\n" % S.end

	""" set geographic boundary for plotting """
	#		[north, east, south, west]
	bound=[max(S.Y), max(S.X), min(S.Y), min(S.X)] # in km 
	cartesian_dist=map(abs,bound) # absolute value
	S.set_geoBoundary(cartesian_dist)

	""" make plots """
	# plot_synth(S,F,"DBZ")
	plot_synth(S,F,"U")
	plot_synth(S,F,"V")
	# plot_synth(S,F,"SPD")
	# plot_synth(S,F,"CONV")
	# plot_synth(S,F,"VOR")

	plt.show()	


def plot_synth(obj,fpath,var):


	if var == 'DBZ':
		cmap_value=[-15,45]
	elif var in ['U','V']:
		cmap_value=[-5,15]
	elif var == 'SPD':
		cmap_value=[5,15]
	else:
		cmap_value=[-1,1]

	# get array
	array=getattr(obj,var)
	zlevel=getattr(obj,'Z')

	# add figure
	fig = plt.figure(figsize=(8,12))

	# store fields and vertical levels
	arrays = [array[:,:,i+1] for i in range(6)]
	levels = [i+1 for i in range(6)]

	plot_grids=ImageGrid( 	fig,111,
						nrows_ncols = (3,2),
						axes_pad = 0.0,
						add_all = True,
						share_all=False,
						label_mode = "L",
						cbar_location = "top",
						cbar_mode="single")

	M = Basemap(		projection='cyl',
						llcrnrlat=obj.lat_bot,
						urcrnrlat=obj.lat_top,
						llcrnrlon=obj.lon_left,
						urcrnrlon=obj.lon_right,
						resolution='i')

	# retrieve coastline
	coastline = M.coastpolygons
	loncoast=coastline[1][0][15:-1]
	latcoast=coastline[1][1][15:-1]

	# flight path
	# fp = zip(*fpath[::20])
	fp = zip(*fpath[::5])
	flight_lat=fp[0]
	flight_lon=fp[1]

	# make gridded plot
	for g,field,k in zip(plot_grids,arrays,levels):

		g.plot(loncoast,latcoast, color='b')
		g.plot(flight_lon,flight_lat)
		g.barbs(-123.5,38.5,5,5)
		im = g.imshow(	field.T,
							interpolation='none',
							origin='lower',
							extent=[	obj.lon_left,
										obj.lon_right,
										obj.lat_bot,
										obj.lat_top ],
							vmin=cmap_value[0],
							vmax=cmap_value[1])
		g.grid(True)
		ztext='MSL='+str(zlevel[k])+'km'
		g.text(	0.1, 0.08,
				ztext,
				fontsize=10,
				horizontalalignment='left',
				verticalalignment='center',
				transform=g.transAxes)


 	
 	# add color bar
 	plot_grids.cbar_axes[0].colorbar(im)

 	fig.suptitle(' Dual-Doppler Synthesis: '+var )

	# show figure
	plt.tight_layout()
	plt.draw()
	



# call main function
if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage()
		exit()
	else:
		main(sys.argv[1], sys.argv[2])