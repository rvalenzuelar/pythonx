

import numpy as np
import gdal
import os
import matplotlib.pyplot as plt


def print_dimensions(datafile):
	print ""
	print "X pixels: %s" % datafile.RasterXSize
	print "Y pixels: %s" % datafile.RasterYSize

def print_georeference(datafile):
	geot = datafile.GetGeoTransform()
	print ""
	print "Origin X: %s" % geot[0]
	print "Origin Y: %s" % geot[3]
	print "pixel width [deg]: %s" % geot[1]
	print "pixel height [deg]: %s\n" % geot[5]



dem_file='/home/raul/Github/pythonx/merged_dem_38-39_123-124_extended.tif'
temp_file='/home/raul/Github/pythonx/temp.tif'
out_file='/home/raul/Github/pythonx/temp_resamp.tif'


if os.path.isfile(temp_file):
	os.remove(temp_file)

if os.path.isfile(out_file):
	os.remove(out_file)


dtmfile = gdal.Open(dem_file)
print_dimensions(dtmfile)
print_georeference(dtmfile)


lon = -123.3
lat = 38.7
ulx = lon - 0.1
uly = lat + 0.1
lrx = lon + 0.1
lry = lat - 0.1
input_param = (ulx, uly, lrx, lry, dem_file, temp_file)
run_gdal = 'gdal_translate -projwin %s %s %s %s %s %s' % input_param
os.system(run_gdal)
dtmfile=None

resamp_to=50
input_param = (resamp_to,resamp_to,temp_file, out_file)
run_gdal = 'gdalwarp -ts %s %s -r near -co "TFW=YES" %s %s' % input_param
os.system(run_gdal)


datafile = gdal.Open(out_file)
print_dimensions(datafile)
print_georeference(datafile)


band=datafile.GetRasterBand(1)
cols=datafile.RasterXSize
rows=datafile.RasterYSize
data=band.ReadAsArray(0,0,cols,rows)
datafile=None

plt.figure()
plt.imshow(data,interpolation='none',cmap='terrain',vmin=0,vmax=800)
plt.colorbar()
plt.draw()

levels=15
dtm_mask=np.zeros((rows,cols,levels))

res=25 # [m] vertical resolution
for ij in np.ndindex(dtm_mask.shape[:2]):
	i,j=ij
	n = int(data[i,j]/res)
	if n > levels:
		dtm_mask[i,j] = 1
	else:
		dtm_mask[i,j,0:n] = 1
	
	# print dtm_mask[i,j]

# print dtm_mask[:,:,5]

plt.figure()
plt.imshow(dtm_mask[:,:,2],interpolation='none')
plt.colorbar()
plt.draw()


plt.show(block=False)

