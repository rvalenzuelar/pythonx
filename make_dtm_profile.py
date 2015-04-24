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


import math

# define global constants	
pi = math.pi
deg2rad = pi/180.0 
rad2deg = 180.0/pi
earth_radius=6371 # [km]

def process_profile():

	import gdal
	from os.path import expanduser
	import numpy as np 

	# handles dem
	home = expanduser("~")
	dem_file = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
	stdtape_file = 
	layer = gdal.Open(dem_file)
	bands = layer.RasterCount
	gt =layer.GetGeoTransform()

	# calculate destination point
	radar_position=(38,1,-123,4)
	tilt_angle=19.5
	startP=[38.44,-123.31]
	heading=90; #[degrees]
	distance=30; #[km]
	finishP = destination(startP,heading,distance)

	# interpolate a line with coordinates
	number_points = 100	
	line=interpolateLine(startP,finishP,number_points)

	# retrieve the altitude at each line point
	altitude=[]
	for point in line:
		altitude.append( getElevation(point[1],point[0],layer,bands,gt) )

	# plot profile
	dist=np.linspace(0,distance,number_points)
	plot_profile(dist,altitude)

def getElevation(x,y,layer,bands,gt):
	
	col=[]
	px = int((x - gt[0]) / gt[1])
	py =int((y - gt[3]) / gt[5])
	for j in range(bands):
		band = layer.GetRasterBand(j+1)
		data = band.ReadAsArray(px,py, 1, 1)
		col.append(data[0][0])
	return col[0]

def interpolateLine(start_point,finish_point,number_points):
	
	from geographiclib.geodesic import Geodesic
	
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

def plot_profile(dist,val):
	import matplotlib.pyplot as plt
	line = plt.plot(dist, val, linewidth=2)
	plt.grid(True)
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
