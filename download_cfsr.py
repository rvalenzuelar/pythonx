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

url_in='{0}/{1}/{2}/{3}/{4}'
url_out='{0}/{1}/{2}'

out_dir='/home/raul/CFSR'

print_str='Downloading ({0}/{1}) {2}'

total = dates.size


for n,date in enumerate(dates):
	y = str(date.year)
	m = str(date.month).zfill(2)
	d = str(date.day).zfill(2)
	H = str(date.hour).zfill(2)

	if not os.path.isdir(out_dir+'/'+y):
		os.makedirs(out_dir+'/'+y)

	file_name = 'pgbhnl.gdas.'+y+m+d+H+'.grb2'
	urli = url_in.format(root,y,y+m,y+m+d,file_name)
	urlo = url_out.format(out_dir,y,file_name)

	print(print_str.format(n+1,total,urlo))
	urllib.urlretrieve(urli,urlo)

