''' 
	Command line utility to make 
	directory structures

	Usage:
	$ python make_dir_structure.py c01 leg01 ...legNN

	Raul Valenzuela
	January 2016
	raul.valenzuela@colorado.edu
'''

import sys
import os

inarg = sys.argv[1:]
paths=[]
for n,s in enumerate(inarg):
	if n == 0:
		paths.append(s)
	else:
		paths.append('./'+paths[0]+'/'+s+'_cor')
		paths.append('./'+paths[0]+'/'+s+'_all')

print ' Making directory paths:'
for p in paths[1:]:
	print p
	os.makedirs(p)
print ' Done\n'



