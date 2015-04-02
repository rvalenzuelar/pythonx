# source:
# http://simplekml.readthedocs.org/en/latest/geometries.html

import simplekml
import numpy as np 

# ini_lat=36.8
# fin_lat=38.8
# ini_lon=-124.5
# fin_lon=-122.5
# n_grid=50

# # grid points
# x_grid=np.linspace( ini_lon, fin_lon, n_grid )
# y_grid=np.linspace( ini_lat, fin_lat, n_grid )

# # create list of tuples coordinates
# xy=[]
# hgt=10.0
# for x in x_grid:
# 	for y in y_grid:
# 		xy.append( (round(x,2),round(y,2),hgt) )

# # create sequence for polygon nodes
# num_nodes=(n_grid*n_grid)-(n_grid+1) # I don't know why but it seems to work
# kernel=np.array([0,1,(n_grid+1),n_grid,0]) # first nodes
# for x in range(num_nodes):
# 	# first tilt in the series
# 	if x==0:
# 		seq=[xy[kernel[0]],xy[kernel[1]],xy[kernel[2]],xy[kernel[3]],xy[kernel[4]]]
# 	elif (x+1)%(n_grid)>0 and (x+1)%(n_grid)<=(n_grid-2):
# 		kernel=kernel+1
# 		seq.extend([xy[kernel[0]],xy[kernel[1]],xy[kernel[2]],xy[kernel[3]],xy[kernel[4]]])
# 	# the last one in a column close at the first row of the next column
# 	elif (x+1)%(n_grid)==(n_grid-1):
# 		kernel=kernel+1
# 		seq.extend([xy[kernel[0]],xy[kernel[1]],xy[kernel[2]],xy[kernel[3]]])
# 	# change in column only updates the kernel
# 	else:
# 		kernel=kernel+1

# # print seq

# # create kml polygon object
# kml = simplekml.Kml()
# pol = kml.newpolygon(name='A Polygon')  

# # populate polygon coords
# pol.outerboundaryis=seq 

# # style
# pol.style.linestyle.color = simplekml.Color.green
# pol.style.linestyle.width = 2
# pol.style.polystyle.fill = 0

# kml.save("Polygon.kml")




import os
import simplekml

# Create an instance of Kml
kml = simplekml.Kml(open=1)

# Create a linestring with two points (ie. a line)
linestring = kml.newlinestring(name="A Line")
linestring.coords = [(-122.364383,37.824664),(-122.364152,37.824322)]

# Create a linestring that will hover 50m above the ground
linestring = kml.newlinestring(name="A Hovering Line")
linestring.coords = [(-122.364167,37.824787,50), (-122.363917,37.824423,50)]
linestring.altitudemode = simplekml.AltitudeMode.relativetoground

# Create a linestring that will hover 100m above the ground that is extended to the ground
linestring = kml.newlinestring(name="An Extended Line")
linestring.coords = [(-122.363965,37.824844,100), (-122.363747,37.824501,100)]
linestring.altitudemode = simplekml.AltitudeMode.relativetoground
linestring.extrude = 1

# Create a linestring that will be extended to the ground but sloped from the ground up to 100m
linestring = kml.newlinestring(name="A Sloped Line")
linestring.coords = [(-122.363604,37.825009,0), (-122.363331,37.824604,100)]
linestring.altitudemode = simplekml.AltitudeMode.relativetoground
linestring.extrude = 1

# Save the KML
kml.save(os.path.splitext(__file__)[0] + ".kml")