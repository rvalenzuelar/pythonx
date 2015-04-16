#
# Display ascii DTM as image
#
# Raul Valenzuela
# April, 2015
#
# Use:
#	$ python display_asc_dtm.py [filename with path]
#

import matplotlib.pyplot as plt
import numpy as np
import sys

filename=sys.argv[1]

# print "name of the file is %s" % filename

filein = open(filename)
try:
	print "Reading lines\n"
	lines = filein.read().split('\n')
finally:
	filein.close()

n=0
linesp=[]
for line in lines[1:-1]:
	n=n+1
	print "Converting to list array in line: %s" % n
	linesp.append(line.split())

print "Converting to numpy array"
dtm=np.asarray(linesp,dtype=np.uint16) # should improve this conversion
print dtm.shape

plt.imshow(dtm)
plt.show()
