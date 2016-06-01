'''
	Script for dowloading CFSR grib via opendap

	Raul Valenzuela
	June, 2016
	raul.valenzuela@colorado.edu
'''
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
from pydap.client import open_url


def iwv_flux(Q,U,V):

	q=Q['data']
	u=U['data']
	v=V['data']
	press=V['pres']

	dP = np.expand_dims(np.diff(press), axis=1)*100. #[Pa]
	g = 9.8  # [m/s2]

	' layer averages '
	ql = (q[:-1, :, :] + q[1:, :, :]) / 2.
	ul = (u[:-1, :, :] + u[1:, :, :]) / 2.
	vl = (v[:-1, :, :] + v[1:, :, :]) / 2.
	' flux per component per layer'
	u_iwvf = (1/g)*ql*ul*dP[:, None]
	v_iwvf = (1/g)*ql*vl*dP[:, None]
	uwvf = np.squeeze(np.sum(u_iwvf, axis=0))
	vwvf = np.squeeze(np.sum(v_iwvf, axis=0))
	' total flux per layer'
	wvf = np.sqrt(np.power(u_iwvf, 2) + np.power(v_iwvf, 2))
	' integrated flux'
	data = np.squeeze(np.sum(wvf, axis=0))
	array = {'data':data,'lats':Q['lats'],'lons':Q['lons'],'pres':press}

	return array

def parse_url(dates):

	root = 'http://nomads.ncdc.noaa.gov/thredds/dodsC/modeldata/cmd_pgbh'

	url_str='{0}/{1}/{2}/{3}/{4}'

	url_list=[]
	for date in dates:
		y = str(date.year)
		m = str(date.month).zfill(2)
		d = str(date.day).zfill(2)
		H = str(date.hour).zfill(2)		
		file_name = 'pgbh00.gdas.'+y+m+d+H+'.grb2'
		url_list.append(url_str.format(root,y,y+m,y+m+d,file_name))

	return url_list

def download_to_array(varname=None,preslvl=None,dates=None,domain=None):

	urls = parse_url(dates)

	for url in urls:
		print url
		dataset = open_url(url)

		print dataset['time'].data 

		lats = dataset['lat'][:]
		lons = dataset['lon'][:]
		pres = dataset['pressure'][:]/100. #[hPa]

		lats_idx = np.where((lats>domain['latn'])&
							(lats<domain['latx']))[0]
		lons_idx = np.where((lons>360+domain['lonn'])&
							(lons<360+domain['lonx']))[0]

		last = lats_idx[0]
		laen = lats_idx[-1]+1
		lost = lons_idx[0]
		loen = lons_idx[-1]+1

		latsnew = lats[lats_idx]
		lonsnew = lons[lons_idx]-360

		if varname == 'UWND':
			v_name = 'U-component_of_wind'
		elif varname == 'VWND':
			v_name = 'V-component_of_wind'
		elif varname == 'SPHU':
			v_name = 'Specific_humidity'
		elif varname == 'GHGT':
			v_name = 'Geopotential_height'
		elif varname == 'TEMP':
			v_name = 'Temperature'

		if preslvl:
			lvl=np.where(pres==preslvl)[0][0]
			data = np.squeeze(dataset[v_name][v_name][:,lvl,last:laen,lost:loen])
			array={'data':data,'lats':latsnew,'lons':lonsnew,'pres':None}
		else:
			data = np.squeeze(dataset[v_name][v_name][:,:,last:laen,lost:loen])
			array={'data':data,'lats':latsnew,'lons':lonsnew,'pres':pres}

		return array

def plot(array,typep=None,clevel=None):

	fig,ax = plt.subplots()

	lats=array['lats']
	lons=array['lons']

	latm,lonm = np.meshgrid(lats,lons)
	latn = np.min(lats)
	latx = np.max(lats)
	lonn = np.min(lons)
	lonx = np.max(lons)

	m = Basemap(projection='merc',
	            llcrnrlat=latn,
	            urcrnrlat=latx,
	            llcrnrlon=lonn,
	            urcrnrlon=lonx,
	            resolution='l',
				ax=ax)

	if typep == 'pcolor':
		m.pcolormesh(lonm.T,latm.T,array['data'],latlon=True)
	elif typep == 'contourf':
		X,Y=m(lonm.T, latm.T)
		m.contourf(X,Y,array['data'],clevel)

	m.drawparallels(lats[1::10],labels=[1,0,0,0])
	m.drawmeridians(lons[1::20],labels=[0,0,0,1])
	m.drawcoastlines()

	plt.show(block=False)


def save_to_file(varname=None,date=None,domain=None,file=None):

	file.attrs['file_name']        = 'myfilename'
	file.attrs['file_time']        = 'mydateadntime'
	file.attrs['creator']          = 'download_opendap_cfsr.py'
	file.attrs['HDF5_Version']     = h5py.version.hdf5_version
	file.attrs['h5py_version']     = h5py.version.version

	array = download_to_array(varname=varname,
								dates=date,
								domain=domain)

	grp = f.create_group('timestamp')
	ds = grp.create_dataset(varname, data=array['data'])
	ds.attrs['units'] = 'someunit'


'''	********************
	Implementation plot
	********************'''

# domain={'latn':20,'latx':55,'lonn':-150,'lonx':-116}

# dates=pd.date_range(start='2004-02-25 06:00',
# 					periods=1,
# 					freq='6H')

# Q = download_to_array(varname='SPHU',dates=dates,domain=domain)
# U = download_to_array(varname='UWND',dates=dates,domain=domain)
# V = download_to_array(varname='VWND',dates=dates,domain=domain)

# ivt = iwv_flux(Q,U,V)

# plot(ivt,typep='contourf',clevel=range(300,1700,200))
# plot(ivt,typep='pcolor')


'''	***************************
	Implementation save to file
	****************************'''

domain={'latn':-57,'latx':-27,'lonn':-110,'lonx':-45} 

dates=pd.date_range(start='2000-01-01 00:00',
					periods=10,
					freq='6H')

f = h5py.File(foofile, "w") 

for d in dates:
	Q = save_to_file(varname='SPHU',date=d,domain=domain,file=f)
	U = save_to_file(varname='UWND',date=d,domain=domain,file=f)
	V = save_to_file(varname='VWND',date=d,domain=domain,file=f)

	# ivt = iwv_flux(Q,U,V)


f.close()