# -*- coding: utf-8 -*-
"""
Demonstrates common image analysis tools.

Many of the features demonstrated here are already provided by the ImageView
widget, but here we present a lower-level approach that provides finer control
over the user interface.
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import gdal
from os.path import expanduser
import matplotlib.cm as cm # colormap

# Update profile
def updatePlot():
    global img, roi, data, p2
    selected = roi.getArrayRegion(data, img)
    # p2.plot(selected.mean(axis=1), clear=True)
    p2.plot(selected, clear=True)
#

def makeLut(ncolors):
	lut_temp=cm.gist_earth(np.arange(ncolors))*256
	return lut_temp[::,0:3].astype(int)

def makeColorbarGradient(levels,lut):

	nlevels = len(levels)
	stops = np.linspace(0,1,nlevels)
	grad = QtGui.QLinearGradient()
	for stop in stops:
		indx=int(stop*255)
		grad.setColorAt(stop,QtGui.QColor(lut[indx,0],lut[indx,1],lut[indx,2]))

	return grad



# create app
pg.mkQApp()

# create window
win = pg.GraphicsLayoutWidget()
win.setWindowTitle('pyqtgraph example: Image Analysis')

# A plot area (ViewBox + axes) for displaying the image
p1 = win.addPlot()

# Item for displaying image data
img = pg.ImageItem()
p1.addItem(img)


# Custom ROI for selecting an image region
# roi = pg.ROI([10, 30], [30, 30])
# roi.addScaleHandle([0.5, 1], [0.5, 0.5])
# roi.addScaleHandle([0, 0.5], [0.5, 0.5])
# roi=pg.PolyLineROI([[20,40],[80,80], [100,100]], closed=False)
# roicoor=[[10, 64], [120,64]]
roi=pg.LineSegmentROI([[10,10],[30,30]])
p1.addItem(roi)
roi.setZValue(100)  # make sure ROI is drawn above image
# roi.movable=False

# # Contrast/color control
grad = pg.GradientEditorItem(orientation='right')
# grad.loadPreset('greyyncolors')
# grad.setColorMap(lut)
# win.addItem(grad,0,1)
# print grad.colorMap()
# win.addItem(cb,0,1)


# Another plot area for displaying ROI data
win.nextRow()
p2 = win.addPlot(colspan=2)
p2.setMaximumHeight(250)
win.resize(600, 700)
win.show()


# handles geotiff dem (1 band only)
home = expanduser("~")
dem_file = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
layer = gdal.Open(dem_file)
gt =layer.GetGeoTransform()

# prepare dtm
clip=[-124.17, -122.65, 37.80, 39.30]
xmin = int((clip[0] - gt[0]) / gt[1])
ymin =int((clip[3] - gt[3]) / gt[5])
xmax = int((clip[1] - gt[0]) / gt[1])
ymax =int((clip[2] - gt[3]) / gt[5])	
win_xsize=xmax-xmin
win_ysize=ymax-ymin
x_buff=200 #new resolution
y_buff=200 #new resolution
data = np.rot90(layer.GetRasterBand(1).ReadAsArray(xmin,ymin,
						win_xsize,win_ysize,
						x_buff,y_buff),3)
lut=makeLut(256)
img.setImage(data,lut=lut,levels=(0,1000))


# colorbar
cb=pg.GradientLegend((10,200), (30,30))
cb.setParentItem(img)
val=np.linspace(0,1000,20).astype(int)
foograd=makeColorbarGradient(val,lut)
cb.setGradient(foograd)
cblabels = {'0': 0,'200':0.2,'400':0.4,
			'600':0.6,'800':0.8,'1000': 1}
cb.setLabels(cblabels)
cb.scale(1,-1)

# set position and scale of image
# img.scale(0.2, 0.2)
# img.translate(-50, 0)

# zoom to fit imageo
p1.autoRange()  


roi.sigRegionChanged.connect(updatePlot)

updatePlot()



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
