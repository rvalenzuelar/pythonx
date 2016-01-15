#!/usr/bin/env python
'''
	Command line utilities for NOAA-D radar files.

	This file has to be located in a directory included
	in the environmental variable PATH

	Raul Valenzuela
	January, 2016
	raul.valenzuela@colorado.edu
'''

import fnmatch
import sys
import os
import shutil
import matplotlib.pyplot as plt

from glob import glob


def main(args):

	if args[1] in ['-h', '--help']:
		usage()
	elif args[1] in ['rhi', 'RHI']:
		if args[2] == 'count':
			count(scan_mode='rhi')
		elif args[2] == 'mkdir':
			make_dir_and_copy(args[3], scan_mode='rhi')
	elif args[1] in ['ppi', 'PPI']:
		if args[2] == 'count':
			count(scan_mode='ppi')
		elif args[2] == 'mkdir':
			make_dir_and_copy(args[3], scan_mode='ppi')
	elif args[1] in ['plot']:
		' implement range-height plot'
		plt.plot([3,5],[3,10])
		plt.show()

def make_dir_and_copy(scan,scan_mode):

	if scan_mode == 'ppi':
		elev=scan
		elevparse=scan.replace('.','')
		elevdir='./elev'+elevparse.zfill(3)
		elevfiles=glob('*.'+elev+'_*')
		if not elevfiles:
			print ' No files with elevation '+elev+' where found\n'
			return 1
		else:
			try:
				os.makedirs(elevdir)
			except OSError:
				print ' Directory already exists\n'
				return 1

			print ' Copying files to '+elevdir
			for f in elevfiles:
				shutil.copy(f,elevdir)
			print ' Done\n'

	elif scan_mode == 'rhi':
		az=scan
		azdir='./az'+az.zfill(3)
		azfiles=glob('*.'+az+'.*')
		if not azfiles:
			print ' No files with azimuth '+az+' where found\n'
			return 1
		else:
			try:
				os.makedirs(azdir)
			except OSError:
				print ' Directory already exists\n'
				return 1
			print ' Copying files to '+azdir
			for f in azfiles:
				shutil.copy(f,azdir)
			print ' Done\n'

def count(scan_mode=None):

	swpfiles=glob('swp*')
	if scan_mode == 'ppi':
		swpfiles=fnmatch.filter(swpfiles,'*_PPI_*')
	elif scan_mode == 'rhi':
		swpfiles=fnmatch.filter(swpfiles,'*_RHI_*')

	' list of scan mode in directory '
	scans=[]
	for swp in swpfiles:
		split=swp.split('.')
		if scan_mode == 'ppi':
			intpart=split[4]
			decpart=split[5][0:1]
			s=intpart+'.'+decpart
		elif scan_mode == 'rhi':
			s=split[4]
		if s not in scans:
			scans.append(s)

	' count of each scan mode '
	scount=[]
	for s in scans:
		if scan_mode == 'ppi':
			filtered=fnmatch.filter(swpfiles,'*.'+s+'_*')
		elif scan_mode == 'rhi':
			filtered=fnmatch.filter(swpfiles,'*.'+s+'.*')
		scount.append(len(filtered))
	
	merged=zip(scans,scount)
	merged.sort(key=lambda tup:tup[1])
	for a,c in merged:
		if scan_mode == 'ppi':
			print 'elev={:>3}, count={:g}'.format(a,c)
		elif scan_mode == 'rhi':
			print 'az={:>3}, count={:g}'.format(a,c)
	return scans


def usage():

	S="""
	This function is located in ~/Github/pythonx (bashrc PATH added).
	It can be called from a directory containing 
	dorade(sweep) files with syntax:
	
	$ radar_utils.py [options]

	options:
		ppi count
		rhi count
		rhi mkdir [azimuth]
		ppi mkdir [elevation]

	"""
	print S

main(sys.argv)