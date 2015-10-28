
from PIL import Image
import glob

fmt_in='.tif'
fmt_out='.png'

base_dir='/home/rvalenzuela/SPROF/CZD98CalCombinedImages'
# base_dir='/home/rvalenzuela/SPROF/CZD01CalCombinedImages'
# base_dir='/home/rvalenzuela/SPROF/CZD03CalCombinedImages'
# base_dir='/home/rvalenzuela/SPROF/CZD04CalCombinedImages'

files_in = glob.glob(base_dir+'/*'+fmt_in)
files_in.sort()

for f in files_in:
	im=Image.open(f)
	fout=f[:-4]+fmt_out
	print fout
	im.save(fout)

print '\nDone'