# Read cfradial file
# 
# See http://www.unidata.ucar.edu/software/netcdf/examples/programs/
#
# Raul Valenzuela
# March, 2015
from netCDF4 import Dataset
import glob
import numpy as np 
import pandas as pd 

# open standard tape file for reading
stdtape_file = Dataset('010125I.nc','r') 

# get stdtape timestamp
base_time=stdtape_file.variables['base_time'][:]
stdtape_secs=stdtape_file.variables['Time'][:]
stdtape_timestamp=pd.to_datetime(stdtape_secs+base_time,unit='s')
stdtape_lats=stdtape_file.variables['LAT'][:]
stdtape_lons=stdtape_file.variables['LON'][:]

# close the file
stdtape_file.close()

# get a list cfradial files
nclist = glob.glob('cfrad.*')

# open cfradial file for reading and writing
cfrad_file = Dataset(nclist[0],'r+') 

# get cfradial timestamp
start_datetime_nparray=cfrad_file.variables['time_coverage_start'][:]
start_datetime_str="".join(start_datetime_nparray)
time_format="%Y-%m-%dT%H:%M:%SZ"
cfrad_start_datetime=pd.to_datetime(start_datetime_str,format=time_format)
cfrad_time = cfrad_file.variables['time'][:]
cfrad_secs=pd.to_timedelta(cfrad_time.astype(int),unit='s')
cfrad_timestamp=cfrad_start_datetime+cfrad_secs

# cfradial coordinates
lats = cfrad_file.variables['latitude'][:]
lons = cfrad_file.variables['longitude'][:]








# print ''
# print cfrad_start_datetime
print ''
print stdtape_lats
print ''
print stdtape_lons
print ''

# close the file.
cfrad_file.close()
