#Slicing

import numpy as np

arr=np.array([5,3,5,7,9,8,7,
              5,3,2,6,8,0,2,
              3,5,6,7,1,0,4])

asize=arr.shape
cols=asize[0]

lowlim=cols/3
upplim=2*cols/3

print cols
print lowlim, upplim
print arr[:lowlim]
print arr[lowlim:upplim]
print arr[upplim:]