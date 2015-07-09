#!/usr/bin/env python

# Raul Valenzuela
# April, 2015
#
# For process_profile and getDtmElevation see:
# http://gis.stackexchange.com/questions/59316/
# python-script-for-getting-elevation-difference-between-two-points
#
# For interpolateLine see:
# http://stackoverflow.com/questions/16015533/get-n-points-on-a-line
#
# For destination see:
# http://www.movable-type.co.uk/scripts/latlong.html
# http://williams.best.vwh.net/avform.htm#LL
#
# For plot_profile (dem subplot) see:
# http://stackoverflow.com/questions/24956653/read-elevation-using-gdal-python-from-geotiff
#

import math
import sys
import getopt 
import gdal
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from subprocess import call
from os.path import expanduser
from os.path import isfile
from geographiclib.geodesic import Geodesic
from netCDF4 import Dataset


# define global constants	
pi = math.pi
deg2rad = pi/180.0 
rad2deg = 180.0/pi
earth_radius=6371 # [km]
home = expanduser("~")
tilt_angle=19.5
distance=45; #[km] beam length
dem_file = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
stdtape_filepath=home+"/Github/correct_dorade_metadata/010123I.nc"

def usage():
	print "\nUsage examples:"
	print "$ ./make_dtm_profile.py -t '2001-01-23 21:46:12' -s 'aft'"
	print "$ ./make_dtm_profile.py -t '2001-01-23 21:46:12' -s 'fore'\n"

def getInputs(argv):
	global time 
	global type_scan

	op0="h" # print usage
	op1="t:" # time
	op2="s:" # type_scan
	myops=op0+op1+op2

	try:
		opts, args = getopt.getopt(argv,myops)
	except getopt.GetoptError:
		usage()
		exit()

	if opts != []:
		for opt, arg in opts:
			if opt == '-h':
					usage()
					exit()
			elif opt in ("-t"):
				time = arg
				# print time
				# exit()
			elif opt in ("-s"):
				type_scan = arg
	else:
		usage()
		exit()

	# if output file already exists deploy it and exist
	outfile="profile_"+time.replace(" ","_")+"_"+type_scan+".png"
	if isfile("./"+outfile):
		# eog is unix utility for visualizing images
		call(["eog", outfile])		
		exit()

def main():

	# handles geotiff dem (1 band only)
	layer = gdal.Open(dem_file)
	gt =layer.GetGeoTransform()

	# radar position and track
	radar_position = getAircraftPosition()

	# calculate destination point
	startP=radar_position[0:2]
	track_angle=radar_position[2]
	heading=calculateHeading(track_angle, type_scan); #[degrees]
	finishP_left = destination(startP,heading[0],distance)
	finishP_right = destination(startP,heading[1],distance)

	# interpolate left and right line with coordinates
	number_points = 150	
	line_left=interpolateLine(startP,finishP_left,number_points)
	line_right=interpolateLine(startP,finishP_right,number_points)

	# retrieve altitude at each line point (left and right)
	altitude_left=getAltitudeProfile(line_left,layer,gt)
	altitude_right=getAltitudeProfile(line_right,layer,gt)
	
	# plot profile
	dist=np.linspace(-distance,distance,number_points*2)
	# line_p=[[startP[1],finishP[1]],[startP[0],finishP[0]]]
	# plot_profile(dist,altitude,line_p,layer,gt,radar_position)
	altitude=[altitude_left,altitude_right]
	finishP=[finishP_left,finishP_right]
	plot_profile(dist,altitude,finishP,layer,gt,radar_position)

def getDtmElevation(x,y,layer,gt):	
	col=[]
	px = int((x - gt[0]) / gt[1])
	py =int((y - gt[3]) / gt[5])
	win_xsize=1
	win_ysize=1
	band = layer.GetRasterBand(1)
	data = band.ReadAsArray(px,py, win_xsize, win_ysize)
	col.append(data[0][0])
	col.append(0)
	return col[0]

def getAltitudeProfile(line,layer,gt):
	altitude=[]
	for point in line:
		altitude.append( getDtmElevation(point[1],point[0],layer,gt) )

	return altitude

def interpolateLine(start_point,finish_point,number_points):
	gd = Geodesic.WGS84.Inverse(start_point[0], start_point[1], 
					finish_point[0], finish_point[1])
	line = Geodesic.WGS84.Line(gd['lat1'], gd['lon1'], gd['azi1'])
	line_points=[];
	for i in range(number_points):
		point = line.Position(gd['s12'] / number_points * i)
		line_points.append((point['lat2'], point['lon2']))

	return line_points

def destination(start_point,heading,distance):
	angular_dist = float(distance) / float(earth_radius) #[radians]
	lat1=start_point[0] # [degrees]
	lon1=start_point[1] # [degrees]

	A = sind(lat1)*cos(angular_dist)
	B = cosd(lat1)*sin(angular_dist)*cosd(heading)
	lat2=asin( A+B ) * rad2deg

	C = sind(heading)*sin(angular_dist)*cosd(lat1)
	D = cos(angular_dist)-sind(lat1)*sind(lat2)
	lon2=( lon1*deg2rad+atan2( C,D ) ) * rad2deg

	return (lat2,lon2)

def getAircraftPosition():
	# open standard tape file for reading
	stdtape_file = Dataset(stdtape_filepath,'r') 

	# get stdtape timestamp
	base_time=stdtape_file.variables['base_time'][:]
	stdtape_secs=stdtape_file.variables['Time'][:]
	stdtape_timestamp=pd.to_datetime(stdtape_secs+base_time,unit='s')
	stdtape_lats=stdtape_file.variables['LAT'][:]
	stdtape_lons=stdtape_file.variables['LON'][:]
	stdtape_track=stdtape_file.variables['TRACK'][:]
	stdtape_galt=stdtape_file.variables['GEOPOT_ALT'][:]
	stdtape_palt=stdtape_file.variables['PRES_ALT'][:]
	

	# close the file
	stdtape_file.close()	

	# pandas dataframe for standar tape
	d={'lats':stdtape_lats,'lons':stdtape_lons,'track': stdtape_track,
		'galt':stdtape_galt, 'palt':stdtape_palt}
	df_stdtape=pd.DataFrame(data=d,index=stdtape_timestamp)

	latRad=df_stdtape[time]['lats'].values
	lonRad=df_stdtape[time]['lons'].values
	track=df_stdtape[time]['track'].values
	galtRad=df_stdtape[time]['galt'].values
	paltRad=df_stdtape[time]['palt'].values
	
	return [latRad[0],lonRad[0],track[0],galtRad[0],paltRad[0]]
	

def getAircraftArrow(radar_position):
	start_point = radar_position[0:2]
	heading = radar_position[2]
	distance = 10.0 # [km]
	end_point = destination(start_point,heading,distance)
	return [ start_point[0] , start_point [1], end_point[0] , end_point[1] ]

def calculateHeading(track_angle, type_scan):
	if type_scan=='fore':
		head_left=track_angle-90+tilt_angle
		head_right=track_angle+90-tilt_angle
	elif type_scan=='aft':
		head_left=track_angle-90-tilt_angle
		head_right=track_angle+90+tilt_angle
	else:
		print 'Error with type scan (aft/fore)'
		exit()
	return [head_left,head_right]


def plot_profile(dist,alt, line_prof, layer, gt,radar_position):
	# interactive mode
	plt.ion()

	#prepare dtm
	clip=[-124.17, -122.65, 37.80, 39.30]
	xmin = int((clip[0] - gt[0]) / gt[1])
	ymin =int((clip[3] - gt[3]) / gt[5])
	xmax = int((clip[1] - gt[0]) / gt[1])
	ymax =int((clip[2] - gt[3]) / gt[5])	
	win_xsize=xmax-xmin
	win_ysize=ymax-ymin
	x_buff=150 #new resolution
	y_buff=150 #new resolution
	dtm = layer.GetRasterBand(1).ReadAsArray(xmin,ymin,
							win_xsize,win_ysize,
							x_buff,y_buff)

	# add figure
	fig = plt.figure()

	#grid for subplot
	gs=gridspec.GridSpec(2,1, height_ratios=[3,1])

	# create axes
	ax1 = fig.add_subplot(gs[0])
	ax2 = fig.add_subplot(gs[1])

	# dem
	im=ax1.imshow(dtm, cmap='gist_earth', extent=clip)

	cbar=plt.colorbar(im,ax=ax1)

	# left line
	X=[radar_position[1],line_prof[0][1]]
	Y=[radar_position[0],line_prof[0][0]]
	ax1.plot(X,Y,linewidth=2,c='r')
	# right line
	X=[radar_position[1],line_prof[1][1]]
	Y=[radar_position[0],line_prof[1][0]]
	ax1.plot(X, Y,linewidth=2,c='r')
	# arrow
	acft=getAircraftArrow(radar_position)	
	ax1.annotate('',xy=(acft[3],acft[2]), xycoords='data', 
			xytext=(acft[1],acft[0]),textcoords='data',
			arrowprops=dict(arrowstyle="->",
					linewidth = 2.0,
					color = 'white') )
	ax1.axis((clip))
	ax1.set_title(time)

	# profile
	part1=alt[0]
	part2=alt[1]
	if radar_position[2]>270:
		alt=np.asarray(part1[::-1]+part2) # reverse and merge list
	else:
		alt=np.flipud(np.asarray(part2+part1)) # reverse and merge list

	pAlt=radar_position[3]
	gAlt=radar_position[4]
	# ax2.plot(dist, alt[1]+alt[0], linewidth=2, c='r')
	ax2.plot(dist, alt, linewidth=2, c='r')
	ax2.plot(0,pAlt,'ro')
	ax2.invert_xaxis()
	ax2.grid(True)
	ax2.set_xlabel('Distance from radar [km]')
	ax2.set_ylabel('Altitude [m]')
	ax2.set_xlim([-45,45])
	ax2.set_xticks(np.linspace(-45,45,95/5))
	ax2.set_ylim([0,pAlt+200])

	ax2.text(-40,1000,'Lat = ')
	ax2.text(-40,800,'Lon = ')
	ax2.text(-40,600,'pAlt = ')

	outfile="profile_"+time.replace(" ","_")+"_"+type_scan+".png"
	plt.savefig(outfile, dpi=150)
	call(["eog", outfile])

def sin(value):
	return math.sin(value)

def cos(value):
	return math.cos(value)

def sind(value):
	return math.sin(value*deg2rad)

def cosd(value):
	return math.cos(value*deg2rad)

def asin(value):
	return math.asin(value)

def atan2(value1,value2):
	return math.atan2(value1,value2)


# call main function
if __name__ == "__main__":
	inargs = sys.argv[1:]	
	if not inargs:
		usage()
		exit()
	else:
		getInputs(inargs)
		main()
