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
import AircraftAnalysis as aa 
import argparse
import numpy.ma as ma

def usage():

	desc="""
------------------------------------------------------------------------------	
Script for plotting NOAA-P3 Dual-Doppler analyses derived
from CEDRIC. 
------------------------------------------------------------------------------
"""
	print desc

def main(filepath, stdfile,plotFields, panelOpt):
	
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
	print "Synthesis start time :%s" % S.start
	print "Synthesis end time :%s\n" % S.end

	""" make plots """

	for f in plotFields:
		plot_synth(S,F,var=f,windb=True, panel=panelOpt)

	plt.show()	


def plot_synth(obj,fpath,**kwargs):

	var=kwargs['var']
	windb=kwargs['windb']
	panel=kwargs['panel']

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
		windb_jump=4
		ztext_size=12
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
		arrays = [array[:,:,i+1] for i in range(6)]
		levels = [i+1 for i in range(6)]
		Uarray = [U[:,:,i+1] for i in range(6)]
		Varray = [V[:,:,i+1] for i in range(6)]

	# define colormap range
	if var == 'DBZ':
		cmap_value=[-15,45]
	elif var in ['U','V']:
		cmap_value=[-5,15]
	elif var == 'SPD':
		cmap_value=[5,15]
	else:
		cmap_value=[-1,1]

	# add figure
	fig = plt.figure(figsize=figure_size)
	
	# geographic boundaries
	lat_bot=min(obj.LAT)
	lat_top=max(obj.LAT)
	lon_left=min(obj.LON)
	lon_right=max(obj.LON)

	plot_grids=ImageGrid( fig,111,
							nrows_ncols = rows_cols,
							axes_pad = 0.0,
							add_all = True,
							share_all=False,
							label_mode = "L",
							cbar_location = "top",
							cbar_mode="single")

	M = Basemap(		projection='cyl',
						llcrnrlat=lat_bot,
						urcrnrlat=lat_top,
						llcrnrlon=lon_left,
						urcrnrlon=lon_right,
						resolution='i')

	# retrieve coastline
	coastline = M.coastpolygons
	loncoast=coastline[1][0][13:-1]
	latcoast=coastline[1][1][13:-1]

	# flight path from standard tape
	jmp=5
	fp = zip(*fpath[::jmp])
	flight_lat=fp[0]
	flight_lon=fp[1]

	# creates iterator group
	group=zip(plot_grids,arrays,levels)
	
	# make gridded plot
	for g,field,k in group:

		g.plot(loncoast,latcoast, color='b')
		g.plot(flight_lon,flight_lat)
		
		im = g.imshow(	field.T,
							interpolation='none',
							origin='lower',
							extent=[	lon_left,
										lon_right,
										lat_bot,
										lat_top ],
							vmin=cmap_value[0],
							vmax=cmap_value[1])
		g.grid(True)
		ztext='MSL='+str(zlevel[k])+'km'
		g.text(	0.1, 0.08,
				ztext,
				fontsize=ztext_size,
				horizontalalignment='left',
				verticalalignment='center',
				transform=g.transAxes)

	if windb:	
 		for g,u,v in zip(plot_grids,Uarray,Varray):
			x=obj.LON[::windb_jump]
			y=obj.LAT[::windb_jump]
			uu= u.T[::windb_jump,::windb_jump]
			vv=v.T[::windb_jump,::windb_jump]
 			g.barbs( x , y , uu , vv ,length=windb_size)
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
	



# call main function
if __name__ == "__main__":

	parser = argparse.ArgumentParser(	description=usage(),
											formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("CEDRICfile", 
							help="CEDRIC synthesis file in netCDF format. \nExample: 03/leg01.cdf")
	parser.add_argument("STDTAPEfile", 
							help="NOAA-P3 standard tape file in netCDF format.\nExample: 010123I.nc")
	parser.add_argument("--panel", 
							type=int, 
							nargs=1,
							help="choose a panel [1-6]")

	group = parser.add_mutually_exclusive_group()

	group.add_argument("--all", 
							action='store_true',
							default=None,
							help="plot all fields (DBZ,SPD,CONV,VOR)")
	group.add_argument("--fields", 
							nargs='+',
							help="specify radar fields to be plotted")	
								
	args = parser.parse_args()	

	if args.all:
		args.fields=['DBZ','SPD','CONV','VOR']

	if args.fields:		
		for f in args.fields:
			if f not in ['DBZ','SPD','CONV','VOR']:
				print "Indicate field(s): DBZ,SPD,CONV,VOR\n"
				exit()

	main(	args.CEDRICfile, 
			args.STDTAPEfile,
			args.fields,
			args.panel)

