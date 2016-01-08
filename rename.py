#!/usr/bin/env python
'''
	Command line utility for renaming files

	Raul Valenzuela
	raul.valenzuela@colorado.edu

'''

import os
import sys
from glob import glob

def main(arg):

	if arg[1] in ['-h', '--help']:
		usage()
	else:

		list_pattern=arg[1]
		search_pattern=arg[2]
		replace_pattern=arg[3]

		' current working directory '
		cwd=os.getcwd()

		' get list with files to process'
		# oldl=glob(cwd+'/*.HDF*')
		oldl=glob(cwd+'/'+list_pattern)

		' make list with new patterns'
		# inpattern='/2000'
		# oupattern='/'
		# newl=[s.replace(inpattern, oupattern) for s in oldl]
		newl=[s.replace(search_pattern, replace_pattern) for s in oldl]

		' rename with new pattern '
		for a,b in zip(oldl,newl):
			print a
			print b
			os.rename(a,b)

def usage():
	s='''
	Usage:

	$ rename.py [list_pattern] [search_pattern] [replace_pattern]

	ex:
	$ rename.py *.HDF* /2000 /
	'''
	print s

main(sys.argv)
