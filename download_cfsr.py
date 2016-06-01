'''
	Script for dowloading CFSR grib 
	data from nomads
	http://nomads.ncdc.noaa.gov/modeldata/cmd_pgbh/

	Raul Valenzuela
	June, 2016
	raul.valenzuela@colorado.edu
'''


import sys 
import urllib
import os 
import pandas as pd

from urlparse import urlparse

start='01-01-2000 00:00'
end = '01-02-2000 00:00'
dates = pd.date_range(start=start,end=end,freq='6H')

root = 'http://nomads.ncdc.noaa.gov/modeldata/cmd_pgbh'

url_string='{0}/{1}/{2}/{3}/{4}'

out_dir='/home/raul/CFSR/'

total = dates.size

print_str='Downloading ({0}/{1}) {2}'

for n,date in enumerate(dates):
	y = str(date.year)
	m = str(date.month).zfill(2)
	d = str(date.day).zfill(2)
	H = str(date.hour).zfill(2)
	file_name = 'pgbhnl.gdas.'+y+m+d+H+'.grb2'
	url = url_string.format(root,y,y+m,y+m+d,file_name)
	print(print_str.format(n+1,total,file_name))
	urllib.urlretrieve(url,out_dir+file_name)

