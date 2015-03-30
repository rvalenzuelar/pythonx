# Read CfRadial in text format and write a CSV file
# with variables (e.g. lat,lon,alt)
#
# Raul Valenzuela
# November 2014

import glob

path='/home/rvalenzuela/P3/CfRadial/case04/'

txtList=glob.glob(path+'*.txt')
txtCount=len(txtList)

# writing file
fileout=open('geo_coords_case04.txt','w')

# counter
fnum=1

while fnum<=txtCount:

	# format file number
	fstr="%03d" % fnum
	
	# open reading file
	filein=open(path+fstr+'.txt','r')
	
	# read line
	line=filein.readline()
	
	# parse info
	fileinname=line[12:63]
	lat=float(line[159:168])*100
	lon=float(line[173:188])*1000
	alt=float(line[193:208])
	
	# print to screen
	print lat, lon, alt
	
	# make output string
	lineout=str(lat)+','+str(lon)+','+str(alt)
	
	# write to output file
	fileout.write(lineout+'\n')
	
	# close reading file
	filein.close()
	
	# counter
	fnum+=1

# close writing file	
fileout.close()




