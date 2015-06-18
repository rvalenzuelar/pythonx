#!//home/rvalenzuela/miniconda/bin/python

# Read netCDF file with pseudo-dual Doppler 
# synthesis and plot variables
#
# Check:
# http://matplotlib.org/examples/axes_grid/demo_axes_grid2.html
# http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array
#
# Raul Valenzuela
# June, 2015

from os import getcwd
from os.path import dirname, basename
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.basemap import Basemap
import sys
import matplotlib.pyplot as plt
import AircraftAnalysis as aa 
import argparse
import scipy.ndimage
import numpy as np 
# import numpy.ma as ma 

def usage():

	desc="""
------------------------------------------------------------------------------	
Script for plotting NOAA-P3 Dual-Doppler analyses derived
from CEDRIC. 
------------------------------------------------------------------------------
"""
	print desc

def main( args ):
	
	filepath = args.ced
	stdfile = args.std
	plotFields = args.field 
	panelNum = args.panel
	sliceNum = args.slice
	sliceOrient = args.orientation
	zoomOpt = args.zoomin

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
	try:
		S=aa.Synthesis(filepath)
	except RuntimeError:
		print "Input Error: check file names\n"
		exit()

	""" creates a std tape """
	T=aa.Stdtape(stdtapedir+stdfile)

	""" creates a flightpath """
	F=T.Flightpath(S.start, S.end)

	""" print shape of attribute arrays """
	# S.print_shapes()

	""" print global attirutes of cedric synthesis """
	# S.print_global_atts()
	

	""" print synthesis time """
	print "Synthesis start time :%s" % S.start
	print "Synthesis end time :%s\n" % S.end

	""" make plots """

	for f in plotFields:
		plot_synth(S,F,
					var=f,
					windb=True,
					panel=panelNum,
					sliceN=sliceNum,
					sliceO=sliceOrient,
					zoomIn=zoomOpt)

	plt.show()	


def plot_synth(obj,fpath,**kwargs):

	var=kwargs['var']
	windb=kwargs['windb']
	panel=kwargs['panel']
	slicen=kwargs['sliceN']
	sliceo=kwargs['sliceO']
	zoomin=kwargs['zoomIn']

	# get array
	array=getattr(obj,var)
	zlevel=getattr(obj,'Z')
	U=getattr(obj,'U')		
	V=getattr(obj,'V')	

	# set some plotting values and stores
	# vertical level in a list of arrays
	if panel:
		figure_size=(8,8)
		rows_cols=(1,1)
		windb_size=6.5
		windb_jump=2
		ztext_size=12
		windv_scale=0.5
		windv_width=2
		arrays = [array[:,:,panel[0]] for i in range(6)]
		levels = [panel[0] for i in range(6)]	
		Uarray = [U[:,:,panel[0]] for i in range(6)]
		Varray = [V[:,:,panel[0]] for i in range(6)]			
	else:
		figure_size=(8,12)
		rows_cols=(3,2)
		windb_size=5
		windb_jump=5
		ztext_size=10
		windv_scale=0.5
		windv_width=2
		arrays = [array[:,:,i+1] for i in range(6)]
		levels = [i+1 for i in range(6)]
		Uarray = [U[:,:,i+1] for i in range(6)]
		Varray = [V[:,:,i+1] for i in range(6)]

	# define colormap range
	if var == 'DBZ':
		cmap_value=[-15,45]
		cmap_name='jet'
	elif var in ['U','V']:
		cmap_value=[-5,15]
		cmap_name='jet'
	elif var == 'SPD':
		cmap_value=[5,15]
		cmap_name='YlGnBu_r'
	else:
		cmap_value=[-1,1]
		cmap_name='jet'

	# general  geographic domain boundaries
	lat_bot=min(obj.LAT)
	lat_top=max(obj.LAT)
	lon_left=min(obj.LON)
	lon_right=max(obj.LON)

	M = Basemap(		projection='cyl',
						llcrnrlat=lat_bot,
						urcrnrlat=lat_top,
						llcrnrlon=lon_left,
						urcrnrlon=lon_right,
						resolution='i')

	# flight path from standard tape
	jmp=5
	fp = zip(*fpath[::jmp])
	flight_lat=fp[0]
	flight_lon=fp[1]

	# zoom-in option
	if zoomin: 
		if zoomin[0] == 'offshore':
			lat_bot=38.1
			lat_top=39.1
			lon_left=-124.1
			lon_right=-122.9
		elif zoomin[0] == 'onshore':
			lat_bot=min(obj.LAT)
			lat_top=max(obj.LAT)
			lon_left=min(obj.LON)
			lon_right=max(obj.LON)		
		maskLat= np.logical_and(obj.LAT >= lat_bot, obj.LAT <= lat_top)
		maskLon= np.logical_and(obj.LON >= lon_left, obj.LON <= lon_right)

	# add figure
	fig = plt.figure(figsize=(figure_size))

	plot_grids=ImageGrid( fig,111,
							nrows_ncols = rows_cols,
							axes_pad = 0.0,
							add_all = True,
							share_all=False,
							label_mode = "L",
							cbar_location = "top",
							cbar_mode="single")

	# retrieve coastline
	coastline = M.coastpolygons
	loncoast=coastline[1][0][13:-1]
	latcoast=coastline[1][1][13:-1]

	# creates iterator group
	group=zip(plot_grids,arrays,levels)
	
	# make gridded plot
	for g,field,k in group:

		g.plot(loncoast,latcoast, color='b')
		g.plot(flight_lon,flight_lat)
		
		if zoomin:
			# field=ma.array(field.data,mask=maskGrid.T)
			field=field[maskLon][:,maskLat]

		im = g.imshow(field.T,
						interpolation='none',
						origin='lower',
						extent=[lon_left,
								lon_right,
								lat_bot,
								lat_top ],
						vmin=cmap_value[0],
						vmax=cmap_value[1],
						cmap=cmap_name)
		g.grid(True)
		ztext='MSL='+str(zlevel[k])+'km'
		g.text(	0.1, 0.08,
				ztext,
				fontsize=ztext_size,
				horizontalalignment='left',
				verticalalignment='center',
				transform=g.transAxes)

		if windb:
			x=obj.LON[::windb_jump]
			y=obj.LAT[::windb_jump]	
			u=Uarray[k-1]
			v=Varray[k-1]
			uu= u.T[::windb_jump,::windb_jump]
			vv=v.T[::windb_jump,::windb_jump]
 			# g.barbs( x , y , uu , vv ,length=windb_size)
 			Q=g.quiver(x,y,uu,vv, units='dots', scale=windv_scale, scale_units='dots',width=windv_width)
 			qk=g.quiverkey(Q,0.8,0.08,10,r'$10 \frac{m}{s}$')
 			g.set_xlim(lon_left,lon_right)
 			g.set_ylim(lat_bot, lat_top)

 	# add color bar
 	plot_grids.cbar_axes[0].colorbar(im)
 	var_title={	'DBZ': 'Reflectivity factor [dBZ]',
 				'SPD': 'Wind speed [m/s]',
 				'VOR': 'Vorticity',
 				'CONV': 'Convergence'}
 	fig.suptitle(' Dual-Doppler Synthesis: '+var_title[var] )

	# show figure
	plt.tight_layout()
	plt.draw()


	# if slicen:
	# 	# add figure
	# 	fig = plt.figure(figsize=(8,10))

	# 	plot_grids=ImageGrid( fig,111,
	# 							nrows_ncols = (3,1),
	# 							axes_pad = 0.0,
	# 							add_all = True,
	# 							share_all=False,
	# 							label_mode = "L",
	# 							cbar_location = "top",
	# 							cbar_mode="single")



# call main function
if __name__ == "__main__":

	parser = argparse.ArgumentParser(	description=usage(),
											formatter_class=argparse.RawTextHelpFormatter)

	""" Mandatory Arguments """
	group_mandatory=parser.add_argument_group('Mandatory arguments')
	group_mandatory.add_argument('--ced','-c',
							metavar='file',
							required=True,
							help=	"netCDF CEDRIC synthesis with format CaseNumber/FileName." \
									"\nExample: c03/leg01.cdf")
	group_mandatory.add_argument('--std','-s' ,
							metavar='file',
							required=True,
							help=	"netCDF NOAA-P3 standard tape file using RAF format." \
									"\nExample: 010123I.nc")
	
	""" Optional Arguments """
	group_optional=parser.add_argument_group('Optional arguments')
	group_optional.add_argument('--panel', '-p',
							metavar='num',
							type=int, 
							nargs=1,
							default=None,
							help="choose a panel (1-6); otherwise plots a figure with 6 panles")
	group_optional.add_argument('--zoomin', '-z',
							metavar='str',
							nargs=1,
							default=None,
							choices=['offshore','onshore'],
							help="zoom-in over a offshore|onshore flight leg")	
	group_fields = group_optional.add_mutually_exclusive_group()
	group_fields.add_argument('--all', '-a',
							action='store_true',
							default=None,
							help="[default] plot all fields (DBZ,SPD,CONV,VOR)")
	group_fields.add_argument('--field', '-f',
							metavar='str',
							nargs='+',
							choices=['DBZ','SPD','CONV','VOR'],
							default=['DBZ','SPD','CONV','VOR'],
							help="specify radar field(s) to be plotted")	

	""" Slice options """
	group_slice=parser.add_argument_group('Slice options')
	group_slice.add_argument('--slice', '-sl',
							metavar='num',
							type=int, 
							nargs=1,
							required=False,
							help="number of slices (they are equally spaced)")
	group_slice.add_argument('--orientation', '-o',
							metavar='str',
							nargs=1,
							required=False,
							help="orientation of slices (zonal, meridional, crossb")

	args = parser.parse_args()	

	if args.slice and (args.orientation is None):
		print "Error Indicate orientation of slices\n"
		exit()

	# main(	args.ced, 
	# 		args.std,
	# 		args.field,
	# 		args.panel,
	# 		args.slice,
	# 		args.orientation,
	# 		args.zoomin)
	main(args)
