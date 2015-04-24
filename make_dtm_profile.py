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


def process_profile():


	import gdal
	from osgeo import osr,ogr
	from os.path import expanduser

	home = expanduser("~")
	demfile = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
	radar_position=(38,1,-123,4)
	tilt_angle=19.5

	layer = gdal.Open(demfile)
	bands = layer.RasterCount
	gt =layer.GetGeoTransform()

	startP=[38.44,-123.31]
	finishP=[38.63,-123.07]
	number_points = 10	
	line=interpolateLine(startP,finishP,number_points)

	# print line

	for point in line:
		print getElevation(point[1],point[0],layer,bands,gt)
		# print point[0],point[1]

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

	for i in range(number_points + 1):
		point = line.Position(gd['s12'] / number_points * i)
		# print((point['lat2'], point['lon2']))
		line_points.append((point['lat2'], point['lon2']))
	return line_points

def destination(start_point,heading,distance):
	
	earth_radius=6371 # [km]



# define global constants
import math
pi = math.pi
deg2rad = pi/180.0 
rad2deg = 180.0/pi

process_profile()