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

def usage():

	desc="""
------------------------------------------------------------------------------	
Script for plotting NOAA-P3 Dual-Doppler analyses derived
from CEDRIC. 
------------------------------------------------------------------------------
"""
	print desc

def main(filepath, stdfile,plotFields):
	
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
		plot_synth(S,F,var=f,windb=True)
		# plot_synth(S,F,var="U")
		# plot_synth(S,F,var="V")
		# plot_synth(S,F,var="SPD")
		# plot_synth(S,F,var="CONV")
		# plot_synth(S,F,var="VOR")

	plt.show()	


def plot_synth(obj,fpath,**kwargs):

	var=kwargs['var']
	windb=kwargs['windb']

	# define colormap range
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

	# geographic boundaries
	lat_bot=min(obj.LAT)
	lat_top=max(obj.LAT)
	lon_left=min(obj.LON)
	lon_right=max(obj.LON)

	plot_grids=ImageGrid( 	fig,111,
						nrows_ncols = (3,2),
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

	# flight path
	# fp = zip(*fpath[::20])
	fp = zip(*fpath[::5])
	flight_lat=fp[0]
	flight_lon=fp[1]

	# store fields and vertical levels
	arrays = [array[:,:,i+1] for i in range(6)]
	levels = [i+1 for i in range(6)]

	# make gridded plot
	for g,field,k in zip(plot_grids,arrays,levels):

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
				fontsize=10,
				horizontalalignment='left',
				verticalalignment='center',
				transform=g.transAxes)

	if windb:
		U=getattr(obj,'U')		
		V=getattr(obj,'V')		
		Uarray = [U[:,:,i+1] for i in range(6)]
		Varray = [V[:,:,i+1] for i in range(6)]

 		for g,u,v in zip(plot_grids,Uarray,Varray):
		
			jump=5
			x=obj.LON[::jump]
			y=obj.LAT[::jump]
			uu= u.T[::jump,::jump]
			vv=v.T[::jump,::jump]
 			g.barbs( x , y , uu , vv ,length=5)
 			g.set_xlim(lon_left,lon_right)
 			g.set_ylim(lat_bot, lat_top)

 	# add color bar
 	plot_grids.cbar_axes[0].colorbar(im)

 	fig.suptitle(' Dual-Doppler Synthesis: '+var )

	# show figure
	plt.tight_layout()
	plt.draw()
	



# call main function
if __name__ == "__main__":

	parser = argparse.ArgumentParser(	description=usage(),
											formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("CEDRICfile", 
							type=str, 
							help="CEDRIC synthesis file in netCDF format. \nExample: 03/leg01.cdf")
	parser.add_argument("STDTAPEfile", 
							type=str, 
							help="NOAA-P3 standard tape file in netCDF format.\nExample: 010123I.nc")
	parser.add_argument("--fields", 
							type=str, 
							nargs='*',
							help="radar fields to be plotted")
	parser.add_argument("--panel", 
							type=int, 
							nargs=1,
							help="choose a panel [1-6]")	
	args = parser.parse_args()	

	main(args.CEDRICfile, args.STDTAPEfile,args.fields)

