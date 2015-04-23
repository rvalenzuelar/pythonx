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

	coords=[];
	new_beam=True
	for line in all_lines:
		if new_beam and "Processing" in line:
			beam_line=line
			new_beam=False
			# print line
		else:
			if "Processing" in line:
				# print coords
				create_kml(beam_line,coords)
				exit()
				beam_line=line
			else:
				# coords_lines.append(line)
				lat=line[23:32]
				lon=line[35:46]
				alt=line[48:]
				coords.append( [lon,lat,alt] )


def create_kml( beam_line , beam_coords ):
	
	kml=open("new_coords_beam.kml","w")
	
	beam_name=beam_line[-40:]
	print beam_name

	insert_kml_header('open',kml)
	# n=0
	for coord in beam_coords[1:]:
		# lin.coords=[coord(1,n),coord(1,n+1)]
		# n+=1
		kml.writelines(coord[0]+','+coord[1]+','+coord[2])
		kml.writelines('\n')
	insert_kml_header('close',kml)
	kml.close()

# def create_plot():


def insert_kml_header(state,file_object):
	
	if state=='open':

		file_object.writelines('<?xml version="1.0" encoding="UTF-8"?>\n')
		file_object.writelines('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
		file_object.writelines('<Document>\n')
		file_object.writelines('<name>010123I_single</name>\n')
		file_object.writelines('<Style id="yellowLineGreenPoly">\n')
		file_object.writelines('<LineStyle>\n')
		file_object.writelines('<color>80FFFFFF</color>\n')
		file_object.writelines('<width>4</width>\n')
		file_object.writelines('</LineStyle>\n')
		file_object.writelines('<PolyStyle>\n')
		file_object.writelines('<color>FF0000FF</color>\n')
		file_object.writelines('</PolyStyle>\n')
		file_object.writelines('</Style>\n')
		file_object.writelines('<Placemark>\n')
		file_object.writelines('<name>flight level</name>\n')
		file_object.writelines('<styleUrl>#yellowLineGreenPoly</styleUrl>\n')
		file_object.writelines('<LineString>\n')
		file_object.writelines('<extrude>1</extrude>\n')
		file_object.writelines('<tessellate>1</tessellate>\n')
		file_object.writelines('<altitudeMode>absolute</altitudeMode>\n')
		file_object.writelines('<coordinates>\n')
	else:
		file_object.writelines('</coordinates>\n')
		file_object.writelines('</LineString>\n')
		file_object.writelines('</Placemark>\n')
		file_object.writelines('</Document>\n')
		file_object.writelines('</kml>\n')
	

# call function
coord_file=sys.argv[1]
read_beam_coord(coord_file)
