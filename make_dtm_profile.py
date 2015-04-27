#
# Raul Valenzuela
# April, 2015
#
# For process_profile and getElevation see:
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

import math
import sys
from os.path import expanduser
import gdal
import numpy as np 
from geographiclib.geodesic import Geodesic
from netCDF4 import Dataset
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from subprocess import call


# inputs
time=sys.argv[1] # yyyy-mm-dd HH:MM:SS
type_scan=sys.argv[2] # 'fore' or 'aft'

# define global constants	
pi = math.pi
deg2rad = pi/180.0 
rad2deg = 180.0/pi
earth_radius=6371 # [km]
home = expanduser("~")
tilt_angle=19.5
distance=45; #[km] beam length
dem_file = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
stdtape_filepath=home+"/Github/navigation/010123I.nc"

def process_profile():
	# handles geotiff dem (1 band only)
	layer = gdal.Open(dem_file)
	gt =layer.GetGeoTransform()

	# radar position and track
	radar_position = getAircraftPosition()

	# calculate destination point
	startP=radar_position[0:2]
	track_angle=radar_position[2]
	heading=calculateHeading(track_angle, type_scan); #[degrees]
	finishP = destination(startP,heading,distance)

	# interpolate a line with coordinates
	number_points = 150	
	line=interpolateLine(startP,finishP,number_points)

	# retrieve the altitude at each line point
	altitude=[]
	for point in line:
		altitude.append( getElevation(point[1],point[0],layer,gt) )

	# plot profile
	dist=np.linspace(0,distance,number_points)
	line_p=[[startP[1],finishP[1]],[startP[0],finishP[0]]]
	plot_profile(dist,altitude,line_p,layer,gt,radar_position)

def getElevation(x,y,layer,gt):	
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

def interpolateLine(start_point,finish_point,number_points):
	line_points=[];
	gd = Geodesic.WGS84.Inverse(start_point[0], start_point[1], 
						finish_point[0], finish_point[1])
	line = Geodesic.WGS84.Line(gd['lat1'], gd['lon1'], gd['azi1'])

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

	return [lat2,lon2]

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

	# close the file
	stdtape_file.close()	

	# pandas dataframe for standar tape
	d={'lats':stdtape_lats,'lons':stdtape_lons,'track': stdtape_track}
	df_stdtape=pd.DataFrame(data=d,index=stdtape_timestamp)

	latRad=df_stdtape[time]['lats'].values
	lonRad=df_stdtape[time]['lons'].values
	track=df_stdtape[time]['track'].values

	return [latRad[0],lonRad[0],track[0]]
	

def getAircraftArrow(radar_position):
	start_point = radar_position[0:2]
	heading = radar_position[2]
	distance = 10.0 # [km]
	end_point = destination(start_point,heading,distance)
	return [ start_point[0] , start_point [1], end_point[0] , end_point[1] ]

def calculateHeading(track_angle, type_scan):
	if type_scan=='fore':
		head=track_angle-90+tilt_angle
	elif type_scan=='aft':
		head=track_angle-90-tilt_angle
	else:
		print 'Error with type scan (aft/fore)'
		exit()
	return head


def plot_profile(dist,val, line_prof, layer, gt,radar_position):
	#prepare dtm
	clip=[-124.17, -122.65, 38.30, 39.30]
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
	ax1.imshow(dtm, cmap='gist_earth', extent=clip)
	ax1.plot(line_prof[0], line_prof[1],linewidth=2,c='r')	
	acft=getAircraftArrow(radar_position)	
	ax1.annotate('',xy=(acft[3],acft[2]), xycoords='data', 
			xytext=(acft[1],acft[0]),textcoords='data',
			arrowprops=dict(arrowstyle="->",
					linewidth = 2.0,
					color = 'white') )
	ax1.axis((clip))
	ax1.set_title(time)

	# profile
	ax2.plot(dist, val, linewidth=2, c='r')
	ax2.invert_xaxis()
	ax2.grid(True)
	ax2.set_xlabel('Distance from radar [km]')
	ax2.set_ylabel('Altitude [m]')

	# show figure
	plt.show()

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
process_profile()
