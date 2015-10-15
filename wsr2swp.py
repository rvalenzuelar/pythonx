
import os
import glob

os.environ['BATCH_MODE'] = ""
os.environ['INPUT_FORMAT'] = "WSR_88D_FORMAT"
os.environ['OUTPUT_FLAGS'] = "NO_CATALOG SWEEP_FILES"
os.environ['DORADE_DIR'] = "/home/rvalenzuela/KMUX/case03/dorade"
os.environ['PROJECT_NAME'] = "NEXRAD"
os.environ['RADAR_NAME'] = "KMUX"

wsr_files=glob.glob('/home/rvalenzuela/KMUX/case03/raw/KMUX*')

wsr_files.sort()
for w in wsr_files:
	os.environ['SOURCE_DEV'] = w
	os.system('xltrsii')
