'''
	Script for renaming files

	Raul Valenzuela
	raul.valenzuela@colorado.edu

	usage:
	$ python rename.py
'''

import os
from glob import glob

' current working directory '
cwd=os.getcwd()

' get list with files to process'
oldl=glob(cwd+'/*.HDF*')

' make list with new patterns'
inpattern='/2000'
oupattern='/'
newl=[s.replace(inpattern, oupattern) for s in oldl]

' rename with new pattern '
for a,b in zip(oldl,newl):
	print a
	print b
	os.rename(a,b)

