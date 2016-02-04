#!/usr/bin/env python
''' 
	Command line utility to make 
	directory structures

	Raul Valenzuela
	January 2016
	raul.valenzuela@colorado.edu
'''

import sys
import os
import argparse

def main():

	args=parse_inargv()

	basedir= args.basedir[0]
	subdirs= args.subdirs
	suffix= args.suffix[0]

	paths=[]
	for s in subdirs:
		paths.append('./'+basedir+'/'+s+suffix)

	print ' Making directory paths:'
	for p in paths:
		print p
		os.makedirs(p)
	print ' Done\n'

def parse_inargv():

	parser = argparse.ArgumentParser(	description=usage() )

	parser.add_argument('-d', nargs=1, type=str, dest='basedir')
	parser.add_argument('-s', nargs='+', type=str, dest='subdirs')
	parser.add_argument('-u', nargs=1, type=str, dest='suffix', default=[''])

	args = parser.parse_args()

	return args


def usage():
	s='''
	Usage:

	$ make_dir_structure -d [dir] -s [subdir1] ... [subdirn] -u [suffix]

	Example:
	$ make_dir_structure.py -d c01 -s leg01 leg02 
	$ make_dir_structure.py -d c01 -s leg01 leg02 -u _cor

	'''

main()
