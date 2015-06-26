# http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array

import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

#-- Generate some data...
x, y, z = np.mgrid[-2:2:0.2, -2:2:0.2, -2:2:0.16]
v = x*np.exp(-x**2-y**2-z**2)


#-- Extract the line...
# Make a line with "num" points...
resolution = 40
x0, y0 = 0, 5 # These are in _pixel_ coordinates!!
x1, y1 = 20, 20
x, y = np.linspace(x0, x1, resolution), np.linspace(y0, y1, resolution)
z=np.linspace(0,25,resolution)
zz=np.array([z,]*resolution)


vi=np.empty([resolution,resolution])

for k in range(resolution):
	foo = scipy.ndimage.map_coordinates(v, [y,x,zz[:,k]])
	vi[k,:]=foo


print ("v shape: {0}".format(v.shape))
print ("x shape: {0}".format(x.shape))
print ("y shape: {0}".format(y.shape))
print ("zz shape: {0}".format(zz.shape))
print ("vi shape: {0}".format(vi.shape))


# #-- Plot...
plt.subplot(2,1,1)
plt.imshow(	v[:,:,15],
		origin='lower',
		extent=[0,20,0,20],
		vmin=-0.1,vmax=0.1)
plt.plot([x0, x1], [y0, y1], 'ro-')
plt.colorbar()

plt.subplot(2,1,2)
plt.imshow(	vi,
		origin='lower',
		extent=[0,20,0,20],
		vmin=-0.1,vmax=0.1)
plt.colorbar()
plt.show(block=False)