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
					windb=args.windv,
					panel=args.panel,
					slicem = args.slicem,
					slicez = args.slicez,
					zoomIn=args.zoomin)
	
	# plt.show(block=False)	
	plt.show()	

def plot_synth(S , F, **kwargs):

	"""creates synthesis plot instance """
	P=ap.SynthPlot()

	"""set variables """
	P.var=kwargs['var']
	P.windb=kwargs['windb']
	P.panel=kwargs['panel']
	P.zoomOpt=kwargs['zoomIn']
	try:
		P.slicem=sorted(kwargs['slicem'],reverse=True)
	except TypeError:
		P.slicem=None
	try:
		P.slicez=sorted(kwargs['slicez'],reverse=True)
	except TypeError:
		P.slicez=None

	""" get array """
	if P.var == 'SPD':
		P.var = 'SPH' # horizontal proyection
	array=getattr(S , P.var)		

	""" set common variables """
	P.zvalues=S.Z
	P.u_array=S.U
	P.v_array=S.V
	P.w_array=S.WVA
	# P.w_array=S.WUP

	""" general  geographic domain boundaries """
	P.set_geographic(S)

	""" flight path from standard tape """
	P.set_flight_level(F)

	""" coast line """
	P.set_coastline()

	""" make horizontal plane plot """
	P.horizontal_plane(field=array)
	

	""" make vertical plane plots """		
	if P.slicem:
		if P.var == 'SPH' :
			P.vertical_plane_velocity(	fieldM=S.SPM, # meridional component
										fieldZ=S.SPZ,
										sliceo='meridional') # zonal component)
		else:
			P.vertical_plane(field=array,sliceo='meridional')	

	if P.slicez:
		if P.var == 'SPH' :
			P.vertical_plane_velocity(	fieldM=S.SPM, # meridional component
										fieldZ=S.SPZ,
										sliceo='zonal') # zonal component)
		else:
			P.vertical_plane(field=array,sliceo='zonal')	
		

"""call main function """
if __name__ == "__main__":

	parser = argparse.ArgumentParser(	description=usage(),
											formatter_class=argparse.RawTextHelpFormatter)

	""" Mandatory Arguments """
	group_mandatory=parser.add_argument_group('Needed')
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
	group_optional=parser.add_argument_group('Options')
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
	group_optional.add_argument('--windv', '-w',
						action='store_true',
						help="include wind vectors")	

	""" Field Arguments """
	group_fields = group_optional.add_mutually_exclusive_group()
	group_fields.add_argument('--all', '-a',
							action='store_true',
							default=None,
							help="[default] plot all fields (DBZ,SPD,CON,VOR)")
	group_fields.add_argument('--field', '-f',
							metavar='str',
							nargs='+',
							choices=['DBZ','SPD','CON','VOR','U','V'],
							default=['DBZ','SPD','CON','VOR'],
							help="specify radar field(s) to be plotted")	


	""" Slice options """
	group_slice=parser.add_argument_group('Slices')
	group_slice.add_argument('--slicez', '-slz',
							metavar='lat (float)',
							type=float, 
							nargs='+',
							required=False,
							help="latitude coordinates for zonal slices")
	group_slice.add_argument('--slicem', '-slm',
						metavar='lon (float)',
						type=float, 
						nargs='+',
						required=False,
						help="longitude coordinates for zonal slices")

	args = parser.parse_args()	

	main(args)
