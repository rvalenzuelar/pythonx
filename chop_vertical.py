	def chop_vertical(self,array):


		lats=self.shrink(self.lats,mask=self.maskLat)
		lons=self.shrink(self.lons,mask=self.maskLon)

		nx,ny,nz=array.shape
		# space=10 #px

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