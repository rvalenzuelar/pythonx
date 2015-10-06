# http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array

import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

#-- Generate some data...
y, x, z = np.mgrid[-2:2:0.2, -2:2:0.1, -2:2:0.16]
v = x*np.exp(-x**2 -y**2 -z**2)


#-- Extract the line...
# Make a line with "num" points...
x0, y0 = 0, 5 # These are in _pixel_ coordinates!!
x1, y1 = 35, 15

hres=80
xi = np.linspace(x0, x1, hres)
yi = np.linspace(y0, y1, hres)
vres=40
zi = np.linspace(0,25,vres)
zz = np.array([zi,]*hres)

vi=np.empty([vres,hres])

for k in range(vres):
	xis = xi
	yis = yi
	zis = zz[:,k]
	foo = scipy.ndimage.map_coordinates(v, [yis,xis,zis])
	vi[k,:]=foo

print ("v shape: {0}".format(v.shape))
print ("x shape: {0}".format(x.shape))
print ("y shape: {0}".format(y.shape))
print ("z shape: {0}".format(y.shape))
print ("zz shape: {0}".format(zz.shape))
print ("vi shape: {0}".format(vi.shape))

xs=np.sort(xi)
ys=np.sort(yi)
dist_along_line=np.sqrt(xs*xs + ys*ys)
dline = dist_along_line - dist_along_line[0]

# #-- Plot...
plt.subplot(1,2,1)
plt.imshow(	v[:,:,15],
		origin='lower',
		extent=[0,v.shape[1],0,v.shape[0]],
		vmin=-0.1,vmax=0.1,
		interpolation='none')
plt.plot([x0, x1], [y0, y1], '-',color='black')
plt.plot(x0,y0,marker='o',color='green')
plt.plot(x1,y1,marker='o',color='red')
plt.xlabel('X')
plt.ylabel('Y')

plt.subplot(1,2,2)
plt.imshow(	vi,
		origin='lower',
		extent=[dline[0],dline[-1],0,25],
		vmin=-0.1,vmax=0.1,
		interpolation='none')
plt.ylabel('Z')
plt.xlabel('Dist along line')
# plt.colorbar()

plt.draw()
plt.show(block=False)