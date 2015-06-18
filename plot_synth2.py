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
import sys
import matplotlib.pyplot as plt
import argparse
import scipy.ndimage
import AircraftAnalysis as aa 
import AircraftPlot as ap

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


def plot_synth(S,F,**kwargs):

	# creates synthesis plot instance
	P=ap.SynthPlot()

	# set variables
	P.var=kwargs['var']
	P.windb=kwargs['windb']
	P.panel=kwargs['panel']
	P.slicen=kwargs['sliceN']
	P.sliceo=kwargs['sliceO']
	P.zoomOpt=kwargs['zoomIn']

	# get array
	array=getattr(S,P.var)
	zlevel=getattr(S,'Z')
	U=getattr(S,'U')		
	V=getattr(S,'V')	

	# set some plotting values and stores
	# vertical level in a list of arrays
	if P.panel:
		P.figure_size=(8,8)
		P.rows_cols=(1,1)
		P.windb_size=6.5
		P.windb_jump=2
		P.ztext_size=12
		P.windv_scale=0.5
		P.windv_width=2
		arrays = [array[:,:,P.panel[0]] for i in range(6)]
		levels = [zlevel[P.panel[0]] for i in range(6)]	
		Uarray = [U[:,:,P.panel[0]] for i in range(6)]
		Varray = [V[:,:,P.panel[0]] for i in range(6)]			
	else:
		P.figure_size=(8,12)
		P.rows_cols=(3,2)
		P.windb_size=5
		P.windb_jump=5
		P.ztext_size=10
		P.windv_scale=0.5
		P.windv_width=2
		arrays = [array[:,:,i+1] for i in range(6)]
		levels = [zlevel[i+1] for i in range(6)]
		Uarray = [U[:,:,i+1] for i in range(6)]
		Varray = [V[:,:,i+1] for i in range(6)]

	# define colormap range
	if P.var == 'DBZ':
		P.cmap_value=[-15,45]
		P.cmap_name='jet'
	elif P.var in ['U','V']:
		P.cmap_value=[-5,15]
		P.cmap_name='jet'
	elif P.var == 'SPD':
		P.cmap_value=[5,15]
		P.cmap_name='YlGnBu_r'
	else:
		P.cmap_value=[-1,1]
		P.cmap_name='jet'

	# general  geographic domain boundaries
	P.set_geographic(S)

	# flight path from standard tape
	P.set_flight_level(F)

	# coast line
	P.set_coastline()

	# make horizontal plane plot
	P.horizontal_plane(arrays,levels,ucomp=Uarray,vcomp=Varray)






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
