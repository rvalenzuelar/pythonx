# Module for dual-Doppler plotting of NOAA P-3 tail radar.
#
#
# Raul Valenzuela
# June, 2015
#

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.ndimage

class SynthPlot(object):

	def __init__(self):
		self.var=None
		self.windb=None
		self.panel=None
		self.slicen=None
		self.sliceo=None
		self.zoomOpt=None	
		self.figure_size=(None,None)
		self.rows_cols=(None,None)
		self.windb_size=None
		self.windb_jump=None
		self.zlevel_textsize=None
		self.geo_textsize=None
		self.windv_scale=None
		self.windv_width=None
		self.cmap_value=None
		self.cmap_name=None
		self.lats=None 
		self.lons=None 
		self.lat_bot=None
		self.lat_top=None
		self.lon_left=None
		self.lon_right=None
		self.loncoast=None
		self.latcoast=None 
		self.flight_lat=None
		self.flight_lon=None
		self.maskLat=None
		self.maskLon=None
		self.minz=None
		self.maxz=None
		self.scale=None
		self.extent_vertical=[]
		self.zvalues=[]


	def set_geographic(self,synth_obj):

		self.lats=synth_obj.LAT
		self.lat_bot=min(synth_obj.LAT)
		self.lat_top=max(synth_obj.LAT)
		
		self.lons=synth_obj.LON 
		self.lon_left=min(synth_obj.LON)
		self.lon_right=max(synth_obj.LON)

	def set_coastline(self):

		M = Basemap(		projection='cyl',
							llcrnrlat=self.lat_bot,
							urcrnrlat=self.lat_top,
							llcrnrlon=self.lon_left,
							urcrnrlon=self.lon_right,
							resolution='i')
		coastline = M.coastpolygons

		self.loncoast= coastline[1][0][13:-1]
		self.latcoast= coastline[1][1][13:-1]

	def zoom_in(self,zoom_type):

		if zoom_type == 'offshore':
			self.lat_bot=38.1
			self.lat_top=39.1
			self.lon_left=-124.1
			self.lon_right=-122.9
		elif zoom_type == 'onshore':
			self.lat_bot=38.1
			self.lat_top=39.1
			self.lon_left=-124.1
			self.lon_right=-122.9	
		self.maskLat= np.logical_and(self.lats >= self.lat_bot, self.lats <= self.lat_top)
		self.maskLon= np.logical_and(self.lons >= self.lon_left, self.lons <= self.lon_right)

	def add_windvector(self,grid_ax,ucomp,vcomp):

		x=self.lons[::self.windb_jump]
		y=self.lats[::self.windb_jump]	
		uu= ucomp.T[::self.windb_jump,::self.windb_jump]
		vv=vcomp.T[::self.windb_jump,::self.windb_jump]
		# g.barbs( x , y , uu , vv ,length=windb_size)
		Q=grid_ax.quiver(x,y,uu,vv, 
							units='dots', 
							scale=self.windv_scale, 
							scale_units='dots',
							width=self.windv_width)
		qk=grid_ax.quiverkey(Q,0.8,0.08,10,r'$10 \frac{m}{s}$')
		grid_ax.set_xlim(self.lon_left,self.lon_right)
		grid_ax.set_ylim(self.lat_bot, self.lat_top)

	def set_flight_level(self,stdtape_obj):

		jmp=5
		fp = zip(*stdtape_obj[::jmp])
		self.flight_lat=fp[0]
		self.flight_lon=fp[1]

	def set_panel(self,option):

		# set some plotting values and stores
		# vertical level in a list of arrays
		if option == 'single':
			self.figure_size=(8,8)
			self.rows_cols=(1,1)
			self.windb_size=6.5
			self.windb_jump=2
			self.zlevel_textsize=12
			self.windv_scale=0.5
			self.windv_width=2

		elif option == 'multi':
			self.figure_size=(8,12)
			self.rows_cols=(3,2)
			self.windb_size=5
			self.windb_jump=5
			self.zlevel_textsize=10
			self.windv_scale=0.5
			self.windv_width=2

		elif option == 'vertical':
			self.figure_size=(12,10)
			self.rows_cols=(self.slicen[0],1)
			self.windb_size=5
			self.windb_jump=5
			self.geo_textsize=12
			self.windv_scale=0.5
			self.windv_width=2

	def set_colormap(self,field):

		# define colormap range
		if field == 'DBZ':
			self.cmap_value=[-15,45]
			self.cmap_name='nipy_spectral'
		elif field in ['U','V']:
			self.cmap_value=[-5,15]
			self.cmap_name='jet'
		elif field == 'SPD':
			self.cmap_value=[5,20]
			self.cmap_name='nipy_spectral'
		else:
			self.cmap_value=[-1,1]
			self.cmap_name='jet'		

	def get_slices(self,array,type_of_slice):

		if type_of_slice == 'horizontal':
			slice_group , vertical_group = self.chop_horizontal(array)
			return slice_group, vertical_group

		elif type_of_slice == 'vertical':
			slice_group , geo_group = self.chop_vertical (array)
			return slice_group, geo_group

	def chop_horizontal(self, array):

		# set  vertical level in a list of arrays
		if self.panel:
			choped_array = [array[:,:,self.panel[0]] for i in range(6)]
			vertical_levels = [self.zvalues[self.panel[0]] for i in range(6)]	
			
		else:
			choped_array = [array[:,:,i+1] for i in range(6)]
			vertical_levels = [self.zvalues[i+1] for i in range(6)]
			

		return choped_array, vertical_levels

	def chop_vertical(self):

		nx,ny,nz=array.shape
		space=10 #px

		lats=self.lats[self.maskLat]
		lons=self.lons[self.maskLon]

		""" creates a vector rng with the range of 
			indices idx to select from array.
		"""
		idx=np.empty(self.slicen[0],dtype=int)
		weight=(self.slicen[0]-1)/2.0
		rng=np.arange(-(space*weight),(space*weight)+1,space)

		""" return a list of slices
		"""
		if self.sliceo[0] == 'zonal':
			mid=np.round(ny/2)
			idx.fill(mid)
			slice_idx=[int(i+k) for (i,k) in zip(idx,rng)]
			slices=[array[:,i,:] for i in slice_idx]
			slice_lats=[lats[i] for i in slice_idx]
			return slices,slice_lats

		elif self.sliceo[0] == 'meridional':
			mid=np.round(nx/2)
			idx.fill(mid)
			slice_idx=[int(i+k) for (i,k) in zip(idx,rng)]
			slices=[array[i,:,:] for i in slice_idx]
			slice_lons=[lons[i] for i in slice_idx]
			return slices,slice_lons

		# elif self.sliceo[0] == 'crossb':


	def adjust_ticklabels(self,g):
		
		g.set_xlim(self.extent_vertical[0], self.extent_vertical[1])
		g.set_ylim(0,self.maxz)
		
		new_xticklabel = [str(np.around(val/self.scale,1)) for val in g.get_xticks()]
		g.set_xticklabels(new_xticklabel)

		new_yticklabel = [str(val) for val in g.get_yticks()]
		new_yticklabel[0]=' '
		new_yticklabel[-1]=' '
		g.set_yticklabels(new_yticklabel)		



	def horizontal_plane(self , field_array ,**kwargs):

		u_array=kwargs['ucomp']
		v_array=kwargs['vcomp']
		self.zvalues=kwargs['zlevels']

		if self.panel:
			self.set_panel('single')
		else:
			self.set_panel('multi')

		self.set_colormap(self.var)

		fig = plt.figure(figsize=(self.figure_size))

		plot_grids=ImageGrid( fig,111,
								nrows_ncols = self.rows_cols,
								axes_pad = 0.0,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single")

		array_group, level_group = self.get_slices(field_array,'horizontal')
		ucomp, level_group = self.get_slices(u_array,'horizontal')
		vcomp, level_group = self.get_slices(v_array,'horizontal')


		# creates iterator group
		group=zip(plot_grids,array_group,level_group)

		# make gridded plot
		z=0
		for g,field,k in group:

			g.plot(self.loncoast, self.latcoast, color='b')
			g.plot(self.flight_lon, self.flight_lat)
			
			if self.zoomOpt:
				self.zoom_in(self.zoomOpt[0])
				field=field[self.maskLon][:,self.maskLat]
			
			im = g.imshow(field.T,
							interpolation='none',
							origin='lower',
							extent=[self.lon_left,
									self.lon_right,
									self.lat_bot,
									self.lat_top ],
							vmin=self.cmap_value[0],
							vmax=self.cmap_value[1],
							cmap=self.cmap_name)
			g.grid(True)
			ztext='MSL='+str(k)+'km'
			g.text(	0.1, 0.08,
					ztext,
					fontsize=self.zlevel_textsize,
					horizontalalignment='left',
					verticalalignment='center',
					transform=g.transAxes)

			self.add_windvector(g,ucomp[z],vcomp[z])
			z+=1

		 # add color bar
		plot_grids.cbar_axes[0].colorbar(im)
		var_title={	'DBZ': 'Reflectivity factor [dBZ]',
					'SPD': 'Wind speed [m/s]',
					'VOR': 'Vorticity',
					'CONV': 'Convergence'}
		fig.suptitle(' Dual-Doppler Synthesis: '+var_title[self.var] )

		# show figure
		plt.tight_layout()
		plt.draw()

	def vertical_plane(self,array,zlevel,**kwargs):

		ucomp=kwargs['ucomp']
		vcomp=kwargs['vcomp']
		wcomp=kwargs['vcomp']
		
		print type(array)
		print type(ucomp)
		print type(vcomp)
		print type(wcomp)

		# mask arrays
		if self.zoomOpt:
			self.zoom_in(self.zoomOpt[0])
			array=array[self.maskLon][:,self.maskLat]
			ucomp=ucomp[self.maskLon][:,self.maskLat]
			vcomp=vcomp[self.maskLon][:,self.maskLat]
			wcomp=wcomp[self.maskLon][:,self.maskLat]
		else:
			print "Vertical slice only available with zoom option.\n"
			sys.exit()

		self.set_panel('vertical')
		self.set_colormap(self.var)

		fig = plt.figure(figsize=(self.figure_size))

		plot_grids=ImageGrid( fig,111,
								nrows_ncols = self.rows_cols,
								axes_pad = 0.0,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single",
								aspect=True)


		field_group , slice_geo = self.get_slices(array)
		uComp , slice_geo = self.get_slices(ucomp)
		vComp , slice_geo = self.get_slices(vcomp)
		verticalComp , slice_geo = self.get_slices(wcomp)


		self.minz=0.25
		self.maxz=5.0
		# scale=maxz*3
		self.scale=10

		zmask= np.logical_and(zlevel >= self.minz, zlevel <= self.maxz)

		if self.sliceo[0] == 'zonal':
			self.extent_vertical=[self.lon_left*self.scale,
									self.lon_right*self.scale,
									self.minz,
									self.maxz ]
			horizontalComp=uComp
		elif self.sliceo[0] == 'meridional':
			self.extent_vertical=[self.lat_bot*self.scale,
									self.lat_top*self.scale,
									self.minz,
									self.maxz ]
			horizontalComp=vComp

		# creates iterator group
		group=zip(plot_grids,
					field_group,
					horizontalComp,
					verticalComp)

		# make gridded plot
		p=0
		for g,field,h_comp,w_comp in group:

			field=field[:,zmask]
			im = g.imshow(field.T,
							interpolation='none',
							origin='lower',
							extent=self.extent_vertical,
							vmin=self.cmap_value[0],
							vmax=self.cmap_value[1],
							cmap=self.cmap_name)
			g.grid(True)

			self.adjust_ticklabels(g)
			
			if np.all((np.asarray(slice_geo)>0)):
				geo_axis='Lat: '
			else:
				geo_axis='Lon: '

			geotext=geo_axis+str(np.round(slice_geo[p],2))
			g.text(	0.03, 0.9,
					geotext,
					fontsize=self.zlevel_textsize,
					horizontalalignment='left',
					verticalalignment='center',
					transform=g.transAxes)

			self.add_windvector(g,h_comp[p],w_comp[p])
			p+=1

		 # add color bar
		plot_grids.cbar_axes[0].colorbar(im)
		var_title={	'DBZ': 'Reflectivity factor [dBZ]',
					'SPD': 'Wind speed [m/s]',
					'VOR': 'Vorticity',
					'CONV': 'Convergence'}
		fig.suptitle(' Dual-Doppler Synthesis: '+var_title[self.var] )

		# show figure
		# plt.tight_layout()
		plt.draw()


