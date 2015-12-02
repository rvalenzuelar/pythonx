'''
Need transform HDF4 to HDF5 using
h4toh5 tool

Raul Valenzuela
December 2015
'''

import h5py
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.basemap import Basemap, cm

hfile='/home/raul/1B01.19971231.00527.7.h5'
f = h5py.File(hfile, 'r')

swath=f['Swath']

lats=swath['Latitude'][()]
lons=swath['Longitude'][()]
scantime=swath['ScanTime']
calcounts=swath['calCounts']
channels=swath['channels']


data=channels[:,:,4]
# data[data==-9999.90039062]=np.nan

''' create figure and axes instances  '''
fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

''' create eq distance cylindrival Basemap instance '''
m = Basemap(projection='cyl',\
			llcrnrlat=-40,urcrnrlat=-20,\
            llcrnrlon=-90,urcrnrlon=-60,\
            resolution='l')


''' draw lines '''
m.drawcoastlines()
m.drawcountries()

''' draw parallels '''
parallels = np.arange(-90.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
''' draw meridians '''
meridians = np.arange(0.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)



''' contours '''
# x, y = m(lons, lats) 
# clevs = np.arange(2,40,2)
# cs = m.contourf(x,y,data,clevs,cmap='nipy_spectral')
# cbar = m.colorbar(cs,location='bottom',pad="5%")

''' colormesh '''
m.pcolormesh(lons, lats, data, latlon=True,cmap='gray')
cb = m.colorbar()

plt.show()
