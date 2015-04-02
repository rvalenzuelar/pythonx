#
# Raul Valenzuela
# April, 2015
#
# source:
# http://simplekml.readthedocs.org/en/latest/geometries.html

import simplekml
import numpy as np 

ini_lat=36.8
fin_lat=38.8
ini_lon=-124.5
fin_lon=-122.5

# nodes along a lat or lon line including
# ini and final lat/lon
n_nodes=100 

# grid points
x_grid=np.linspace( ini_lon, fin_lon, n_nodes )
y_grid=np.linspace( ini_lat, fin_lat, n_nodes )

# create list of tuples coordinates
xy=[]
hgt=10.0
for x in x_grid:
	for y in y_grid:
		xy.append( (round(x,2),round(y,2),hgt) )

# create sequence for polygon nodes
total_nodes=(n_nodes*n_nodes)-(n_nodes+1) # I don't know why but it seems to work
kernel=np.array([0,1,(n_nodes+1),n_nodes]) # (first nodes that make a tilt)
for x in range(total_nodes):
	# first tilt in the series
	if x==0:
		seq=[xy[kernel[0]],xy[kernel[1]],xy[kernel[2]],xy[kernel[3]],xy[kernel[0]]]
	elif (x+1)%(n_nodes)!=0:
		kernel=kernel+1
		seq.extend([xy[kernel[0]],xy[kernel[1]],xy[kernel[2]],xy[kernel[3]],xy[kernel[0]]])
	# change in column only updates the kernel
	else:
		kernel=kernel+1

# print seq[10:15]

# total number of tilts
n_tilts=(n_nodes-1)*(n_nodes-1)

# number of nodes that make a tilt (closed polygon)
nodes_per_tilt=5

# create kml object
kml = simplekml.Kml()

# index counter
ix=0
for x in range(n_tilts):
	# create polygon objects for each tilt	
	pol = kml.newpolygon(name='tilt_'+str(x+1))  

	# populate polygon coords
	pol.outerboundaryis=seq[ix:ix+nodes_per_tilt]
	ix=ix+nodes_per_tilt

	# style
	pol.style.linestyle.color = simplekml.Color.green
	pol.style.linestyle.width = 2
	pol.style.polystyle.fill = 0

kml.save("Polygon.kml")