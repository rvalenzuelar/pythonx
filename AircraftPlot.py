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
		self.ztext_size=None
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

	def horizontal_plane(self , array_group , level_group,**kwargs):

		ucomp=kwargs['ucomp']
		vcomp=kwargs['vcomp']

		fig = plt.figure(figsize=(self.figure_size))

		plot_grids=ImageGrid( fig,111,
								nrows_ncols = self.rows_cols,
								axes_pad = 0.0,
								add_all = True,
								share_all=False,
								label_mode = "L",
								cbar_location = "top",
								cbar_mode="single")
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
					fontsize=self.ztext_size,
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

	def vertical_plane(self):
		print "coming soon\n"

		# if slicen:
		# 	# add figure
		# 	fig = plt.figure(figsize=(8,10))

		# 	plot_grids=ImageGrid( fig,111,
		# 							nrows_ncols = (3,1),
		# 							axes_pad = 0.0,
		# 							add_all = True,
		# 							share_all=False,
		# 							label_mode = "L",
		# 							cbar_location = "top",
		# 							cbar_mode="single")


