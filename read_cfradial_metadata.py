#!//home/rvalenzuela/miniconda/bin/python

# Read cfradial metadata
# 
#
# Raul Valenzuela
# May, 2015

from netCDF4 import Dataset
import pandas as pd 
from os import listdir
from os.path import isfile, join, abspath, basename
import sys

def usage():

	S="""
	This function is copied from ~/Github/pythonx to ~/bin.
	Thus, it can be called from a directory containing 
	cfrad files or from any directory with syntax:
	
	$ read_cfradial_metadata.py . (current directory)
	or
	$ read_cfradial_metadata.py [full path to cfradial directory]
	"""

	print S

def main(input_dir):
	
	# input folder
	# cfrad_set="leg03_cor"
	# mypath="/home/rvalenzuela/P3_v2/cfrad/c03/"+cfrad_set
	mypath=input_dir

	# list of files
	cfrad_list = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	
	# get a list cfradial files
	nlist=len(cfrad_list)

	# creates dataframe with name of columns
	cols=(	'lats',
		'lons',
		'alt_msl',
		'alt_agl',
		'ew_vel',
		'nw_vel',
		'vert_vel',
		'head',
		'roll',
		'pitch',
		'drift',
		'rot',
		'tilt',
		'uwin',
		'vwin',
		'wwin')
	df = pd.DataFrame(columns=cols)

	current_path=abspath(mypath)
	print ' Reading metadata in'
	print ' '+current_path
	for f in range(nlist):
		# open cfradial file for reading and writing
		cfrad_file = Dataset(mypath+"/"+cfrad_list[f],'r') 

		# get cfradial timestamp
		start_datetime_nparray=cfrad_file.variables['time_coverage_start'][:20]
		start_datetime_str="".join(start_datetime_nparray)
		time_format="%Y-%m-%dT%H:%M:%SZ"
		
		# each sweep last 6 seconds (~470 values); 
		# metadata values will be averaged and start time 
		# will be the timestamp
		cfrad_start_datetime=pd.to_datetime(start_datetime_str,format=time_format)

		# uncomment if timestamp for individual beams is needed
		#---------------------------------------------------------------------------------------
		# cfrad_time = cfrad_file.variables['time'][:]
		# cfrad_secs=pd.to_timedelta(cfrad_time.astype(int),unit='s')
		# cfrad_timestamp=cfrad_start_datetime+cfrad_secs
		#----------------------------------------------------------------------------------------

		# cfradial metadata averages (ASIB block)
		latitude 	= average(cfrad_file.variables['latitude'][:])
		longitude 	= average(cfrad_file.variables['longitude'][:])
		altitude_msl 	= average(cfrad_file.variables['altitude'][:])
		altitude_agl 	= average(cfrad_file.variables['altitude_agl'][:]	)
		ew_velocity 	= average(cfrad_file.variables['eastward_velocity'][:])
		nw_velocity 	= average(cfrad_file.variables['northward_velocity'][:])
		vert_velocity 	= average(cfrad_file.variables['vertical_velocity'][:])
		heading 	= average(cfrad_file.variables['heading'][:])
		roll 		= average(cfrad_file.variables['roll'][:])
		pitch 		= average(cfrad_file.variables['pitch'][:])
		drift 		= average(cfrad_file.variables['drift'][:])
		rotation		= average(cfrad_file.variables['rotation'][:])
		tilt 		= average(cfrad_file.variables['tilt'][:])
		u_wind		= average(cfrad_file.variables['eastward_wind'][:])
		v_wind		= average(cfrad_file.variables['northward_wind'][:])
		w_wind	= average(cfrad_file.variables['vertical_wind'][:])

		# pandas dataframe for cfradial file
		d={	'lats': latitude,
			'lons': longitude,
			'alt_msl': altitude_msl,
			'alt_agl': altitude_agl,
			'ew_vel': ew_velocity,
			'nw_vel': nw_velocity,
			'vert_vel': vert_velocity,
			'head': heading,
			'roll': roll,
			'pitch': pitch,
			'drift': drift,
			'rot': rotation,
			'tilt': tilt,
			'uwin': u_wind,
			'vwin': v_wind,
			'wwin': w_wind }

		# df_cfrad=pd.DataFrame(data=d,index=cfrad_start_datetime)
		# df_cfrad_new=df_cfrad.copy()
		df.loc[cfrad_start_datetime] = pd.Series(d)


		# close the file.
		cfrad_file.close()

	df.sort(ascending=True, inplace=True)
	
	print ' Exporting to Excel file:'
	# outpath='/home/rvalenzuela/cfradial_metadata_'+cfrad_set+'.xlsx'
	outpath=current_path+'/'+basename(current_path)+'_metadata.xlsx'
	print ' '+outpath
	df.to_excel(outpath,sheet_name='Sheet1')
	print ' Done'

def average(list_of_values):
	return sum(list_of_values)/float(len(list_of_values))

# call main function
if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage()
		exit()
	else:
		main(sys.argv[1])