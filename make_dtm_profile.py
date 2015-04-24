#
# Raul Valenzuela
# April, 2015
#


def process_profile():

	import math
	import gdal
	from osgeo import osr,ogr

	demfile = '/home/raul/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
	radar_position=(38,1,-123,4)
	tilt_angle=19.5
	deg2rad=math.pi/180.0

	layer = gdal.Open(demfile)
	bands = layer.RasterCount
	gt =layer.GetGeoTransform()


	# # creates a new geometry
	# line = ogr.Geometry(ogr.wkbLineString)

	# # add points to line
	# line.AddPoint(-123.31,38.44)
	# line.AddPoint(-123.07,38.63)

	# # # creates a new spatial reference
	# # spatialRef = osr.SpatialReference()

	# kml = line.ExportToKML()

	# print kml




def getValDTM(x,y,layer,bands,gt):
	col=[]
	px = int((x - gt[0]) / gt[1])
	py =int((y - gt[3]) / gt[5])
	for j in range(bands):
		band = layer.GetRasterBand(j+1)
		data = band.ReadAsArray(px,py, 1, 1)
		col.append(data[0][0])
	return col

process_profile()