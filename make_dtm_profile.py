#
# Raul Valenzuela
# April, 2015
#
# See:
#
# http://gis.stackexchange.com/questions/59316/
# python-script-for-getting-elevation-difference-between-two-points
#
#
# http://stackoverflow.com/questions/16015533/get-n-points-on-a-line

def process_profile():

	import math
	import gdal
	from osgeo import osr,ogr
	from os.path import expanduser
	home = expanduser("~")

	demfile = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
	radar_position=(38,1,-123,4)
	tilt_angle=19.5
	deg2rad=math.pi/180.0

	layer = gdal.Open(demfile)
	bands = layer.RasterCount
	gt =layer.GetGeoTransform()

	# print getElevation(-123.101384, 38.666681,layer,bands,gt)

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


process_profile()