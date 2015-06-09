#!//home/rvalenzuela/miniconda/bin/python

# Read netCDF file with pseudo-dual Doppler 
# synthesis and plot variables
#
# Raul Valenzuela
# June, 2015

from netCDF4 import Dataset
from os import getcwd
from os.path import dirname, basename
import sys
import numpy as np
import matplotlib.pyplot as plt

def usage():

	S=	"""
		This function is copied from ~/Github/pythonx to ~/bin.
		Thus, it can be called from a directory containing 
		netCDF4 files or from any directory with syntax:
			
		$ read_cfradial_metadata.py [full path to netCDF file]
		"""
	print S



def main(filepath):
	
	# input folder
	mypath=dirname(filepath)
	myfile=basename(filepath)

	if mypath ==".":
		mypath=getcwd()
	if not myfile:
		print "Please include filename in path"
		exit()

	# creates synthesis object
	S=Synthesis()

	# assign attributes from netCDF file
	S.read_variables(filepath)
	
	# creates 3D cartesian grid
	S.make_grid()

	print_shapes(S)

	im=plt.imshow(S.DBZ[:,:,5],interpolation='none',origin='lower')
	plt.show()
	

def print_shapes(synth_obj):

	print "\nArray shapes:"
	print "--------------------"
	print "X = %d" % synth_obj.X.shape
	print "Y = %d" % synth_obj.Y.shape
	print "Z = %d" % synth_obj.Z.shape
	print "DBZ = (%d,%d,%d)\n" % synth_obj.DBZ.shape

class Synthesis(object):
	def __init__(self):
		self.X=[]
		self.Y=[]
		self.Z=[]
		self.U=[]
		self.V=[]
		self.WUP=[]
		self.WVA=[]
		self.VOR=[]
		self.DIV=[]
		self.DBZ=[]
		self.XG=[]
		self.YG=[]
		self.ZG=[]

	def read_variables(self, filepath):

		# open netCDF file for reading and writing
		synth = Dataset(filepath,'r') 

		# read variable and assing to attribute
		self.X=synth.variables['x'][:]
		self.Y=synth.variables['y'][:]
		self.Z=synth.variables['z'][:]
		self.U=np.squeeze(synth.variables['F2U'][:])
		self.V=np.squeeze(synth.variables['F2V'][:])
		self.WUP=np.squeeze(synth.variables['WUPF2'][:])
		self.WVA=np.squeeze(synth.variables['WVARF2'][:])
		self.VOR=np.squeeze(synth.variables['VORT2'][:])
		self.DIV=np.squeeze(synth.variables['CONM2'][:])
		self.DBZ=np.squeeze(synth.variables['MAXDZ'][:])

		# close netCDF  file.
		synth.close()

		# adjust axis to fit X,Y,Z dimensions
		self.DBZ=np.rollaxis(self.DBZ,2,start=0)
		self.DBZ=np.rollaxis(self.DBZ,2,start=1)

	def make_grid(self):

		self.XG,self.YG,self.ZG=np.meshgrid(self.X,self.Y,self.Z)


# call main function
if __name__ == "__main__":
	if len(sys.argv) == 1:
		usage()
		exit()
	else:
		main(sys.argv[1])