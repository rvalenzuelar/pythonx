#!//home/rvalenzuela/miniconda/bin/python

# Read cfradial metadata
# 
#
# Raul Valenzuela
# May, 2015

from netCDF4 import Dataset
# import glob
import numpy as np 
import pandas as pd 
from os import listdir
from os.path import isfile, join

def main():
	
	mypath="/home/rvalenzuela/P3_v2/cfrad/c03/leg03_cor"
	cfrad_list = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	
	# get a list cfradial files
	nlist=len(cfrad_list)

	for f in range(5):
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
		print cfrad_start_datetime

		 # uncomment if timestamp is need
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

		print heading, roll, pitch, u_wind, v_wind, w_wind

		# # pandas dataframe for cfradial file
		# d={'lats':cfrad_lats,'lons':cfrad_lons}
		# df_cfrad=pd.DataFrame(data=d,index=cfrad_timestamp)
		# df_cfrad_new=df_cfrad.copy()

		# for t in np.arange(nstamps):
		# 	timestamp=str(unique_timestamp[t])
		# 	new_lats=df_stdtape[timestamp]['lats']
		# 	new_lons=df_stdtape[timestamp]['lons']
		# 	df_cfrad_new.loc[timestamp,'lats']=new_lats
		# 	df_cfrad_new.loc[timestamp,'lons']=new_lons


		# cfrad_file.variables['latitude'][:]=df_cfrad_new['lats'].values
		# cfrad_file.variables['longitude'][:]=df_cfrad_new['lons'].values


		# close the file.
		cfrad_file.close()

def average(list_of_values):
	return sum(list_of_values)/float(len(list_of_values))

# call main function
if __name__ == "__main__":
	main()