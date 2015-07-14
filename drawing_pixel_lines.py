import numpy as np 
import demo_interpolate_pixels_along_line as interp 
import matplotlib.pyplot as plt


A=np.zeros((101,101))

p0=(15,12)
p1=(85,55)

coords=interp.xiaoline(p0[0],p0[1],p1[0],p1[1])
for c in coords:
	A[c]=1

A[p0]=0.2
A[p1]=0.8

plt.figure()
plt.imshow(A.T,interpolation='none',
				origin='lower',
				cmap='gist_earth_r',
				vmin=0,
				vmax=1)
plt.grid(which='major')
plt.xlabel('X')
plt.ylabel('Y')
plt.text(p0[0],p0[1],'0',fontsize=18,color='r')
plt.text(p1[0],p1[1],'1',fontsize=18,color='r')
plt.show()



