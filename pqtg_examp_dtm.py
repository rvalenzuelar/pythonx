
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import gdal
from os.path import expanduser


app = QtGui.QApplication([])

## Create window with ImageView widget
win = QtGui.QMainWindow()
win.resize(800,800)
win.setWindowTitle('Digital Terrain Model Profiler')
win.show()

# imageView instance
imv = pg.ImageView()
win.setCentralWidget(imv)


# roi = pg.LineSegmentROI([[10, 64], [120,64]], pen='r')
# imv.addItem(roi)

# handles geotiff dem (1 band only)
home = expanduser("~")
dem_file = home+'/Github/RadarQC/merged_dem_38-39_123-124_extended.tif'
layer = gdal.Open(dem_file)
gt =layer.GetGeoTransform()

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
data = layer.GetRasterBand(1).ReadAsArray(xmin,ymin,
						win_xsize,win_ysize,
						x_buff,y_buff)

# def update():
# 	global data, imv
# 	d = roi.getArraySlice(np.transpose(data), imv.imageItem, axes=(0,))
# 	imv.setImage(d)

# roi.sigRegionChanged.connect(update)

## Display the data 
imv.setImage(np.transpose(data),autoRange=False)

# update()


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
