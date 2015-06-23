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
		self.slice_type=None


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

	def add_windvector(self,grid_ax,comp1,comp2):


		if self.slice_type == 'horizontal':
			xjump=self.windb_jump
			yjump=self.windb_jump

			lons=self.shrink(self.lons,mask=self.maskLon)
			x=self.resample(lons,res=xjump)

			lats=self.shrink(self.lats,mask=self.maskLat)
			y=self.resample(lats,res=yjump)

			uu=self.resample(comp1.T,xres=xjump,yres=yjump)
			vv=self.resample(comp2.T,xres=xjump,yres=yjump)

			Q=grid_ax.quiver(x,y,uu,vv, 
								units='dots', 
								scale=self.windv_scale, 
								scale_units='dots',
								width=self.windv_width)
			qk=grid_ax.quiverkey(Q,0.8,0.08,10,r'$10 \frac{m}{s}$')
			grid_ax.set_xlim(self.lon_left,self.lon_right)
			grid_ax.set_ylim(self.lat_bot, self.lat_top)			

		elif self.slice_type == 'vertical':

			if self.sliceo == 'zonal':
				lons=self.shrink(self.lons,mask=self.maskLon)
				x=self.resample(lons,res=2)
			elif self.sliceo == 'meridional':
				lats=self.shrink(self.lats,mask=self.maskLat)
				x=self.resample(lats,res=2)

			zvalues=self.shrink(self.zvalues,mask=self.zmask)
			y=self.resample(zvalues,res=2)

			hor= self.resample(comp1.T,xres=2,yres=2)
			ver= self.resample(comp2.T,xres=2,yres=2)

			Q=grid_ax.quiver(x*self.scale,y, hor, ver,
								units='dots', 
								scale=0.5, 
								scale_units='dots',
								width=1.5)
			qk=grid_ax.quiverkey(Q,0.95,0.8,10,r'$10 \frac{m}{s}$')
			grid_ax.set_xlim(self.extent_vertical[0],self.extent_vertical[1])
			grid_ax.set_ylim(self.extent_vertical[2], self.extent_vertical[3])			
	
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
		elif field in ['SPH','SPD']:
			if self.slice_type == 'horizontal':
				self.cmap_value=[5,20]
				self.cmap_name='Accent'
			else:
				self.cmap_value=[0,15]
				self.cmap_name='Accent'			
		else:
			self.cmap_value=[-1,1]
			self.cmap_name='jet'		

	def shrink(self,array, **kwargs):

		if len(kwargs)==1:
			array=array[kwargs['mask']]

		elif len(kwargs)==2:
			MaskDimX=kwargs['xmask']
			MaskDimY=kwargs['ymask']			
			array=array[MaskDimX][:,MaskDimY]

		return array

	def resample(self,array,**kwargs):

		if len(kwargs)==1:
			array=array[::kwargs['res']]

		elif len(kwargs)==2:
			xjump=kwargs['xres']
			yjump=kwargs['yres']						
			array= array[::xjump,::yjump]
		return array

			

	def get_slices(self,array):

		if self.slice_type == 'horizontal':
			slice_group , vertical_group = self.chop_horizontal(array)
			return slice_group, vertical_group

		elif self.slice_type == 'vertical':
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

	def chop_vertical(self,array):

		# array=array[self.maskLon][:,self.maskLat]
		# lats=self.lats[self.maskLat]
		# lons=self.lons[self.maskLon]

		lats=self.lats
		lons=self.lons

		nx,ny,nz=array.shape
		space=10 #px

		""" creates a vector rng with the range of 
			indices idx to select from array.
		"""
		idx=np.empty(self.slicen[0],dtype=int)
		weight=(self.slicen[0]-1)/2.0
		rng=np.arange(-(space*weight),(space*weight)+1,space)

		""" return a list of slices
		"""
		if self.sliceo == 'zonal':
			mid=np.round(ny/2)
			idx.fill(mid)
			slice_idx=[int(i+k) for (i,k) in zip(idx,rng)]
			slice_idx.reverse() # slice from north to south
			slices=[array[:,i,:] for i in slice_idx]
			slice_lats=[lats[i] for i in slice_idx]
			return slices,slice_lats

		elif self.sliceo == 'meridional':
			mid=np.round(nx/2)
			idx.fill(mid)
			slice_idx=[int(i+k) for (i,k) in zip(idx,rng)]
			slices=[array[i,:,:] for i in slice_idx]
			slice_lons=[lons[i] for i in slice_idx]
			return slices,slice_lons

		# elif self.sliceo == 'crossb':

	def adjust_ticklabels(self,g):
		
		g.set_xlim(self.extent_vertical[0], self.extent_vertical[1])
		g.set_ylim(0,self.maxz)
		
		new_xticklabel = [str(np.around(val/self.scale,1)) for val in g.get_xticks()]
		g.set_xticklabels(new_xticklabel)

		new_yticklabel = [str(val) for val in g.get_yticks()]
		new_yticklabel[0]=' '
		new_yticklabel[-1]=' '
		g.set_yticklabels(new_yticklabel)		

	def add_slice_line(self,axis,array):

		print self.sliceo
		foo,slice_coord=self.chop_vertical(array)

		print slice_coord



	def horizontal_plane(self , field_array ,**kwargs):

		u_array=kwargs['ucomp']
		v_array=kwargs['vcomp']
		self.zvalues=kwargs['zlevels']

		if self.panel:
			self.set_panel('single')
		else:
			self.set_panel('multi')

		self.slice_type='horizontal'
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

		if self.zoomOpt:
			self.zoom_in(self.zoomOpt[0])
			field_array=self.shrink(field_array,xmask=self.maskLon,ymask=self.maskLat)
			u_array=self.shrink(u_array,xmask=self.maskLon,ymask=self.maskLat)
			v_array=self.shrink(v_array,xmask=self.maskLon,ymask=self.maskLat)

		field_group, level_group = self.get_slices(field_array)
		ucomp, level_group = self.get_slices(u_array)
		vcomp, level_group = self.get_slices(v_array)

		# creates iterator group
		group=zip(plot_grids,level_group,field_group,ucomp,vcomp)

		# make gridded plot
		for g,k,field,u,v in group:

			g.plot(self.loncoast, self.latcoast, color='b')
			g.plot(self.flight_lon, self.flight_lat)		


			# if self.var == 'SPH':
			# 	u.mask=field.mask
			# 	v.mask=field.mask
			
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

			# self.add_windvector(g,u,v)

			# self.slice_type='vertical'
			# foo , slice_geo = self.get_slices(field)

			# print slice_geo
			# self.add_slice_line(g,field)

			g.grid(True)
			ztext='MSL='+str(k)+'km'
			g.text(	0.1, 0.08,
					ztext,
					fontsize=self.zlevel_textsize,
					horizontalalignment='left',
					verticalalignment='center',
					transform=g.transAxes)

		 # add color bar
		plot_grids.cbar_axes[0].colorbar(im)
		fig.suptitle(' Dual-Doppler Synthesis: '+ self.get_var_title(self.var) )

		# show figure
		plt.tight_layout()
		plt.draw()

	def vertical_plane(self,field_array,**kwargs):

		u_array=kwargs['ucomp']
		v_array=kwargs['vcomp']
		w_array=kwargs['wcomp']
		self.zvalues=kwargs['zlevels']

		self.slice_type='vertical'
		self.set_panel(self.slice_type)
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
	


		field_array=self.shrink(field_array,xmask=self.maskLon,ymask=self.maskLat)
		u_array=self.shrink(u_array,xmask=self.maskLon,ymask=self.maskLat)
		v_array=self.shrink(v_array,xmask=self.maskLon,ymask=self.maskLat)
		w_array=self.shrink(w_array,xmask=self.maskLon,ymask=self.maskLat)

		field_group , slice_geo = self.get_slices(field_array)
		uComp , slice_geo = self.get_slices(u_array)
		vComp , slice_geo = self.get_slices(v_array)
		verticalComp , slice_geo = self.get_slices(w_array)


		self.minz=0.25
		self.maxz=5.0
		self.zmask= np.logical_and(self.zvalues >= self.minz, self.zvalues <= self.maxz)

		self.scale=10
		if self.sliceo == 'zonal':
			self.extent_vertical=[self.lon_left*self.scale,
									self.lon_right*self.scale,
									self.minz,
									self.maxz ]
			horizontalComp=uComp

		elif self.sliceo == 'meridional':
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

			if self.var in ['SPD','SPH']:
				field.mask=w_comp.mask

			field=field[: ,self.zmask]
			h_comp=h_comp[: ,self.zmask]
			w_comp=w_comp[: ,self.zmask]

			im = g.imshow(field.T,
							interpolation='none',
							origin='lower',
							extent=self.extent_vertical,
							vmin=self.cmap_value[0],
							vmax=self.cmap_value[1],
							cmap=self.cmap_name)
			# self.add_windvector(g,h_comp,w_comp)

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
			p+=1

			# print "field", field.T[:,50]
			# print "hcomp", h_comp.T[:,50]
			# print "wcomp", w_comp.T[:,50]
			# print "-----------------------"
			# print "sqrt", np.sqrt(h_comp.T[:,50]**2+w_comp.T[:,50]**2)

			# im = g.imshow(field.T,
			# 	interpolation='none',
			# 	origin='lower',
			# 	# extent=self.extent_vertical,
			# 	vmin=self.cmap_value[0],
			# 	vmax=self.cmap_value[1],
			# 	cmap=self.cmap_name)

		 # add color bar
		plot_grids.cbar_axes[0].colorbar(im)
		fig.suptitle(' Dual-Doppler Synthesis: '+self.get_var_title(self.var) )

		# show figure
		# plt.tight_layout()
		plt.draw()
		

	def get_var_title(self,var):
		var_title={	'DBZ': 'Reflectivity factor [dBZ]',
					'SPD': 'Total wind speed [m/s]',
					'SPH': 'Horizontal wind speed [m/s]',
					'VOR': 'Vorticity',
					'CONV': 'Convergence',
					'U': 'wind u-component [m/s]',
					'V': 'wind v-component [m/s]'}
		title=var_title[var]
		
		if self.slice_type == 'vertical' and self.sliceo == 'zonal':
			title = title.replace("Horizontal ","Zonal ")
		elif self.slice_type == 'vertical' and self.sliceo  == 'meridional':
			title = title.replace('Horizontal','Meridional')

		return title