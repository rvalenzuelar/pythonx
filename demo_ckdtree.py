
import numpy as np
from scipy.spatial import cKDTree


lat1=np.linspace(38.1,38.5,10)
lon1=np.linspace(-123.1,-123.8,10)

data1=zip(lat1,lon1)

lat2=np.linspace(38.1,38.5,100)
lon2=np.linspace(-123.1,-123.8,100)

data2=zip(lat2,lon2)

''' search radius '''
r=0.02

t = cKDTree(data2)
d, idx = t.query(data1, k=3, eps=0, p=2, distance_upper_bound=r)

print data1

print d

print idx

print data1[1]
print data2[11]



