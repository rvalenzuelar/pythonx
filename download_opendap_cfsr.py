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
from datetime import datetime


cfsr_prefix = 'pgbhnl.gdas.'

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
	try:
		for date in dates:
			y = str(date.year)
			m = str(date.month).zfill(2)
			d = str(date.day).zfill(2)
			H = str(date.hour).zfill(2)		
			file_name = cfsr_prefix+y+m+d+H+'.grb2'
			url_list.append(url_str.format(root,y,y+m,y+m+d,file_name))
	except TypeError:
		'it is only one timestamp'
		date=dates
		y = str(date.year)
		m = str(date.month).zfill(2)
		d = str(date.day).zfill(2)
		H = str(date.hour).zfill(2)		
		file_name = 'pgbhnl.gdas.'+y+m+d+H+'.grb2'
		url_list.append(url_str.format(root,y,y+m,y+m+d,file_name))

	return url_list

def read_opendap_index(date=None,domain=None):

	url = parse_url(date)

	dataset = open_url(url[0])

	lats = dataset['lat'][:]
	lons = dataset['lon'][:]
	pres = dataset['pressure'][:]/100. #[hPa]

	lats_idx = np.where((lats>domain['latn'])&
						(lats<domain['latx']))[0]
	lons_idx = np.where((lons>360+domain['lonn'])&
						(lons<360+domain['lonx']))[0]

	if domain['preslvl'] is not None:
		pres_idx = np.where(pres==domain['preslvl'])[0][0]
		pres = pres[pres_idx]
	else:
		pres_idx = None


	last = lats_idx[0]
	laen = lats_idx[-1]+1
	lost = lons_idx[0]
	loen = lons_idx[-1]+1

	latsnew = lats[lats_idx]
	lonsnew = lons[lons_idx]-360

	index={'last':last,'laen':laen,'lost':lost,'loen':loen,'plvl':pres_idx}
	coords={'lats':latsnew,'lons':lonsnew,'pres':pres}

	return index,coords

def download_to_array(varname=None,dates=None,indexs=None):

	last = indexs['last']  
	laen = indexs['laen']
	lost = indexs['lost']
	loen = indexs['loen']
	plvl = indexs['plvl']

	urls = parse_url(dates)

	for url in urls:

		dataset = open_url(url)

		if varname == 'UWND':
			v_name = 'U-component_of_wind'
		elif varname == 'VWND':
			v_name = 'V-component_of_wind'
		elif varname == 'TEMP':
			v_name = 'Temperature'
		elif varname == 'RLHU':
			v_name = 'Relative_humidity'
		elif varname == 'GHGT':
			v_name = 'Geopotential_height'
		elif varname == 'GANL':
			v_name = 'Geopotential_height_anomaly'
		elif varname == 'VORT':
			v_name = 'Absolute_vorticity'
		elif varname == 'SPHU':
			v_name = 'Specific_humidity'
		elif varname == 'MSLP':
			v_name = 'Pressure_msl'

		if plvl is None:
			# array = np.squeeze(dataset[v_name][v_name][:,:,last:laen,lost:loen])
			array = dataset[v_name][v_name][:,:,last:laen,lost:loen]
		else:
			array = np.squeeze(dataset[v_name][v_name][:,plvl,last:laen,lost:loen])

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

def new_file(name=None,coords=None):

	file = h5py.File(name, "w") 
	file.attrs['script']   = 'download_opendap_cfsr.py'
	file.attrs['HDF5_Version']     = h5py.version.hdf5_version
	file.attrs['h5py_version']     = h5py.version.version
	file.attrs['cfsr_prefix']      = cfsr_prefix[:-1]

	grp = file.create_group('coords')
	grp.create_dataset('lats', data=coords['lats'])
	grp.create_dataset('lons', data=coords['lons'])
	grp.create_dataset('pres', data=coords['pres'])

	return file

def save_to_file(data=None,timestamp=None,file=None):

	atts = {'UWND':{'name':'U-component of wind','units':'m/s'},
			'VWND':{'name':'V-component of wind','units':'m/s'},
			'TEMP':{'name':'Temperature','units':'K'},
			'RLHU':{'name':'Relative humidity','units':'%'},
			'GHGT':{'name':'Geopotential Height','units':'gpm'},
			'GANL':{'name':'Geopotential Height Anomaly','units':'gpm'},
			'VORT':{'name':'Absolute vorticity','units':'1/s'},
			'SPHU':{'name':'Specific_humidity','units':'kg/kg'},
			'MSLP':{'name':'Mean sea level pressure','units':'Pa'}
			}

	if not '/serie' in file:
		serie = file.create_group('serie')
	else:
		serie = file['/serie']

	grp = serie.create_group(timestamp.strftime('%Y%m%d%H'))

	for k,v in data.iteritems():
		ds = grp.create_dataset(k, data=v)
		ds.attrs['name'] = atts[k]['name']
		ds.attrs['units'] = atts[k]['units']

def run_plot():
	'''
	********************
	Implementation plot
	********************'''

	domain={'latn':20,'latx':55,'lonn':-150,'lonx':-116}

	dates=pd.date_range(start='2004-02-25 06:00',
						periods=1,
						freq='6H')

	Q = download_to_array(varname='SPHU',dates=dates,domain=domain)
	U = download_to_array(varname='UWND',dates=dates,domain=domain)
	V = download_to_array(varname='VWND',dates=dates,domain=domain)

	ivt = iwv_flux(Q,U,V)

	plot(ivt,typep='contourf',clevel=range(300,1700,200))
	plot(ivt,typep='pcolor')


def run_save_to_file():
	'''	
	***************************
	Implementation save to file
	****************************'''

	t0=datetime.now()

	domain={'latn':-57,'latx':-27,
			'lonn':-110,'lonx':-45,
			'preslvl':None} 

	# dates=pd.date_range(start='2000-01-01 00:00',
	# 					periods=1464,
	# 					freq='6H')

	dates=pd.date_range(start='2000-03-29 12:00',
						end  ='2000-12-31 18:00',
						freq ='6H')

	total_files = dates.size
	print_str='Downloading ({0}/{1}) {2}'

	indexs,coords = read_opendap_index(date=dates[0],domain=domain)

	dates_except = []

	for n,d in enumerate(dates):

		print(print_str.format(n+1,total_files,d))

		fname = '/localdata/CFSR_SA/CFSR_SA_'+d.strftime('%Y%m%d%H')+'.h5'

		try:
			Q = download_to_array(varname='SPHU',dates=d,indexs=indexs)
			U = download_to_array(varname='UWND',dates=d,indexs=indexs)
			V = download_to_array(varname='VWND',dates=d,indexs=indexs)
			T = download_to_array(varname='TEMP',dates=d,indexs=indexs)
			R = download_to_array(varname='RLHU',dates=d,indexs=indexs)
			G = download_to_array(varname='GHGT',dates=d,indexs=indexs)
			A = download_to_array(varname='GANL',dates=d,indexs=indexs)
			O = download_to_array(varname='VORT',dates=d,indexs=indexs)
			M = download_to_array(varname='MSLP',dates=d,indexs=indexs)

			# data={'SPHU':Q,'UWND':U,'VWND':V}

			data={	'SPHU':Q,'UWND':U,'VWND':V,
					'TEMP':T,'RLHU':R,'GHGT':G,
					'GANL':A,'VORT':O,'MSLP':M,}

			f = new_file(name=fname,coords=coords)
			save_to_file(data=data,timestamp=d,file=f)
			f.close()
		except:
			print 'Problem with {}'.format(d)
			dates_except.append(d)

	print dates_except

	t1=datetime.now()
	td=t1-t0
	print 'Saving time elapsed: {} seconds'.format(td.seconds)

run_save_to_file()