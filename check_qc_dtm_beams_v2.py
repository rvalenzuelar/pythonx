#!/usr/bin/python

# Read dumped coordinates from runapp.sh and creates 
# kml files or plots to check beam profiles 
#
# Raul Valenzuela
# April, 2015

import sys 

def read_beam_coord( coord_file ):

	filein=open(coord_file,'r')
	all_lines=filein.read().split('\n')
	filein.close()

	coords=[]
	new_beam=True
	for line in all_lines:
		if new_beam and "Processing" in line:
			beam_line=line
			new_beam=False
			# print line
		else:
			if "Processing" in line:
				
				create_kml(beam_line,coords)
				# exit()
				beam_line=line
				coords=[]
			else:
				lat=float(line[23:32])
				lon=float(line[35:46])
				alt=float(line[48:])
				coords.append( (lon,lat,alt) )


def create_kml( beam_line , beam_coords ):

	import simplekml
	import os

	# beam_name=beam_line[-40:]
	beam_name = os.path.basename(beam_line)

	kml=simplekml.Kml()

	print beam_name
		
	for coord in beam_coords[::10]:
		pnt = kml.newpoint()	
		pnt.coords=[coord]
	pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
	pnt.style.labelstyle.scale = 0.5

	# kml.save('beam_with_points.kml')
	kml.save(beam_name+'.kml')


# def create_plot():

	

# call function
coord_file=sys.argv[1]
read_beam_coord(coord_file)
