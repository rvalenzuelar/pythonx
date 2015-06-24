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
	panelNum = args.panel
	sliceCoords = args.slice
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
					sliceCoords=sliceCoords,
					zoomIn=zoomOpt)

	plt.show()	


def plot_synth(S , F, **kwargs):

	# creates synthesis plot instance
	P=ap.SynthPlot()

	# set variables
	P.var=kwargs['var']
	P.windb=kwargs['windb']
	P.panel=kwargs['panel']
	P.zoomOpt=kwargs['zoomIn']
	# P.slice=kwargs['sliceCoords']
	P.slice=sorted(kwargs['sliceCoords'],reverse=True)

	# get array
	if P.var == 'SPD':
		P.var = 'SPH' # horizontal proyection
	array=getattr(S , P.var)		
	zlevel=getattr(S , 'Z')
	U=getattr(S , 'U')		
	V=getattr(S , 'V')	
	W=getattr(S , 'WVA')	
	# W=getattr(S,'WUP')

	
	""" general  geographic domain boundaries """
	P.set_geographic(S)

	""" flight path from standard tape """
	P.set_flight_level(F)

	""" coast line """
	P.set_coastline()

	""" make horizontal plane plot """
	P.horizontal_plane(field=array,zlevels=S.Z,ucomp=U,vcomp=V,wcomp=W)
	

	""" make vertical plane plots """
	if P.slice:
		if P.var == 'SPH' :
			if all(i>90 for i in P.slice):
				P.vertical_plane(field=getattr(S , 'SPM'),zlevels=S.Z,ucomp=U,vcomp=V,wcomp=W)
			elif all(i<90 for i in P.slice):		
				P.vertical_plane(field=getattr(S , 'SPZ'),zlevels=S.Z,ucomp=U,vcomp=V,wcomp=W)
			else:
				print "all coordinates in lat or lon"
				exit()
		else:
			P.vertical_plane(field=array,zlevels=S.Z,ucomp=U,vcomp=V,wcomp=W)
		
	
		



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
							help="[default] plot all fields (DBZ,SPD,CON,VOR)")
	group_fields.add_argument('--field', '-f',
							metavar='str',
							nargs='+',
							choices=['DBZ','SPD','CON','VOR','U','V'],
							default=['DBZ','SPD','CON','VOR'],
							help="specify radar field(s) to be plotted")	

	""" Slice options """
	group_slice=parser.add_argument_group('Slice options')
	group_slice.add_argument('--slice', '-sl',
							metavar='cooordinate (lat or lon)',
							type=float, 
							nargs='+',
							required=False,
							help="coordinates for slices; both values are positive floats")

	args = parser.parse_args()	

	main(args)
