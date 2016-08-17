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
import numpy as np

from datetime import datetime
from glob import glob


def main(args):

    if args[1] in ['-h', '--help']:
        usage()
    elif args[1] in ['rhi', 'RHI']:
        if args[2] == 'count':
            if len(args[1:]) == 2:
                count(scan_mode='rhi')
            elif args[3] == 'sort':
                count(scan_mode='rhi', sort=True)
        elif args[2] == 'mkdir':
            make_dir_and_copy(args[3], scan_mode='rhi')
    elif args[1] in ['ppi', 'PPI']:
        if args[2] == 'count':
            if len(args[1:]) == 2:
                count(scan_mode='ppi')
            elif args[3] == 'sort':
                count(scan_mode='ppi', sort=True)
        elif args[2] == 'mkdir':
            make_dir_and_copy(args[3], scan_mode='ppi')
    elif args[1] in ['beam_plot']:
        ' implement range-height plot'
        # plt.plot([3,5],[3,10])
        # plt.show()
        beam_hgt(args[2])


def make_dir_and_copy(scan, scan_mode):

    if scan_mode == 'ppi':
        elev = scan
        elevparse = scan.replace('.', '')
        elevdir = './elev' + elevparse.zfill(3)
        elevfiles = glob('*.' + elev + '_*')
        if not elevfiles:
            print ' No files with elevation ' + elev + ' where found\n'
            return 1
        else:
            try:
                os.makedirs(elevdir)
            except OSError:
                print ' Directory already exists\n'
                return 1

            print ' Copying files to ' + elevdir
            for f in elevfiles:
                shutil.copy(f, elevdir)
            print ' Done\n'

    elif scan_mode == 'rhi':
        az = scan
        azdir = './az' + az.zfill(3)
        azfiles = glob('*.' + az + '.*')
        if not azfiles:
            print ' No files with azimuth ' + az + ' where found\n'
            return 1
        else:
            try:
                os.makedirs(azdir)
            except OSError:
                print ' Directory already exists\n'
                return 1
            print ' Copying files to ' + azdir
            for f in azfiles:
                shutil.copy(f, azdir)
            print ' Done\n'


def count(scan_mode=None, sort=False):

    swpfiles = glob('swp*')
    if scan_mode == 'ppi':
        swpfiles = fnmatch.filter(swpfiles, '*_PPI_*')
    elif scan_mode == 'rhi':
        swpfiles = fnmatch.filter(swpfiles, '*_RHI_*')
    # print swpfiles
    ' list of scan mode in directory '
    scans = []
    for swp in swpfiles:

        split = swp.split('.')

        if scan_mode == 'ppi':
            elev_intpart = split[4]
            elev_decpart = split[5][0:1]
            angle = elev_intpart + '.' + elev_decpart
        elif scan_mode == 'rhi':
            angle = split[4]

        if angle not in scans:
            scans.append(angle)

    ' count of each scan mode and get beg and end times '
    scount = []
    begs = []
    ends = []
    for s in scans:
        if scan_mode == 'ppi':
            filtered = fnmatch.filter(swpfiles, '*.' + s + '_*')
        elif scan_mode == 'rhi':
            filtered = fnmatch.filter(swpfiles, '*.' + s + '.*')
        count = len(filtered)
        scount.append(count)
        beg, end = get_beg_end_times(filtered)
        begs.append(beg)
        ends.append(end)

    scans = [str(s).zfill(3) for s in scans]
    merged = zip(scans, scount, begs, ends)
    if sort:
        merged.sort(key=lambda tup: tup[0])
    else:
        merged.sort(key=lambda tup: tup[1])
    ppi_strfmt = 'elev={:>4}, count={:>3}, beg={:%Y-%m-%d %H:%M:%S}, end={:%Y-%m-%d %H:%M:%S}'
    rhi_strfmt = 'az={:>3}, count={:>3}, beg={:%Y-%m-%d %H:%M:%S}, end={:%Y-%m-%d %H:%M:%S}'
    for angle, count, be, en in merged:
        if scan_mode == 'ppi':
            print ppi_strfmt.format(angle, count, be, en)
        elif scan_mode == 'rhi':
            print rhi_strfmt.format(angle.lstrip('0'), count, be, en)
    return scans


def get_beg_end_times(file_list):

    file_list.sort()
    raw_beg = file_list[0].split('.')[1][1:]
    raw_end = file_list[-1].split('.')[1][1:]

    fmt = '%y%m%d%H%M%S'
    beg = datetime.strptime(raw_beg, fmt)
    end = datetime.strptime(raw_end, fmt)

    return beg, end


def beam_hgt(target_elev):

    import pandas as pd

    H = []
    ranges = np.arange(0, 101)
    elev_angles = range(0, 11)  # [deg]
#    vert_beam_width = 1.  # [deg]

    fig, ax = plt.subplots()

    te = float(target_elev)
    el = [float(te)] * len(ranges)
    H_target = map(beamhgt_stdrefraction, ranges, el)
    ax.plot(ranges, H_target, color='r')
    for e in elev_angles:
        el = [float(e)] * len(ranges)
        H = map(beamhgt_stdrefraction, ranges, el)
        ax.plot(ranges, H, color='b')
        ax.text(ranges[50], H[50], str(e))
    ax.set_xticks(np.arange(0, 100, 10))
    ax.set_yticks(np.arange(0, 12, 0.5))
    ax.set_ylim([0, 10])
    ax.set_xlim([0, 100])
    ax.set_xlabel('range [km]')
    ax.set_ylabel('beam height AGL [km]')
    plt.grid(True)
    plt.show()

    S = pd.Series(H_target,index=ranges)
    return S

def beamhgt_stdrefraction(r, el):
    ' From Rinehart p. 62'

    ER = 6371  # [km] Earth Radius
    R = (4 / 3.) * ER
    Ho = 0  # [km] radar's altitude
    # print [r,el]
    r2 = r*r
    R2 = R*R
    sin =  np.sin(el*np.pi/180.)
    return np.sqrt(r2 + R2 + 2*r*R*sin) - R + Ho


def usage():

    S = """
    This function is located in ~/Github/pythonx (bashrc PATH added).
    It can be called from a directory containing
    dorade(sweep) files with syntax:

    $ radar_utils.py [options]

    options:
        ppi count
        ppi count sort (sort by elevation)
        rhi count
        rhi count sort (sort by azimuth)
        rhi mkdir [azimuth]
        ppi mkdir [elevation]
        beam_plot [elevation]

    """
    print S

main(sys.argv)
