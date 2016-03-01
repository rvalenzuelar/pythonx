'''
    Script for creating backups using rsync
    Copy only if files in source have changed or if
    they are new.

    Raul Valenzuela
    raul.valenzuela@colorado.edu
'''

import subprocess
from ctext import ctext

DIRS = ['ANALYSES/',
        'BALLOON/',
        'BUOY/',
        'CFSR/',
        'GOES/',
        'GPS_IWV/',
        'P3_analysis/',
        'P3_soundings/',
        'P3_stdtape/',
        'P3_v2/',
        'SPROF/',
        'SSMI/',
        'SURFACE/',
        'WINDPROF/',
        'XPOL/']

SOURCE = '/mnt/rvalenzuela/'
DESTINATION = '/localdata/'

rsync_opts = "-uav"

for D in DIRS:
    src = SOURCE + D
    dest = DESTINATION + D
    print ctext('copying from {} to {}'.format(src, dest)).green()
    subprocess.call(["rsync", rsync_opts, src, dest])
