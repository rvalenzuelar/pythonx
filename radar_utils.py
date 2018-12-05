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
import xarray as xr
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
        beam_hgt(args[2:])


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

    xmax = 30  # [km] max range
    ymax = 10 # [km] max altitude
    Ho = 0.010 # [km] radar height
    beam_width = 2.7  # [deg]
    max_range = 30

    te = map(float,target_elev)

    H = []

    ranges = np.arange(0, max_range+0.25, 0.25)
    # elev_angles = np.array([0, 0.5]+range(1, 15))  # [deg]
    elev_angles = np.round(np.arange(0, 100, 0.1), 1)  # [deg]

    rans, eles = np.meshgrid(ranges, elev_angles)
    beams = beamhgt_stdrefraction(rans, eles, Ho)
    da = xr.DataArray(beams.T,coords=[ranges, elev_angles],
                    dims=['range','elev'])

    fig, ax = plt.subplots()

    ''' reference elevation angles '''
    # elang = list(elev_angles)

    # range_loc = 50  # [km]
    # h_loc = list(beams[:-1,range_loc])
    # try:
    #     rem = [elang.index(x) for x in te]
    #     nones=[h_loc.pop(x) for x in rem]
    # except ValueError:
    #     pass
    
    # try:
    #     nones = [elang.remove(e) for e in te]
    # except:
    #     pass

    ''' add reference elevations '''
    # ha=ax.contour(rans,beams,eles,
    #               levels=elang,
    #               colors='b')

    ''' add labels to beams '''
    # da=xr.DataArray(beams.T,coords=[rans[0,:], eles[:,0]],
    #                 dims=['rans','eles'])
    # for el in elev_angles[1:6]:
    #     ysel = da.sel(rans=xmax, eles=el)        
    #     ax.text(xmax, ysel, str(el), ha='left',va='center', 
    #             color='b', weight='bold')

    # return rans, beams, eles

    # locations=zip([range_loc]*len(h_loc), 
    #                 h_loc)
    # plt.clabel(ha,fmt='%1.1f',
    #             # manual=locations
    #             )



    # for el in  elev_angles[8:]:
    #     xsel = da.sel(rans=ymax, eles=el)        
    #     ax.text(xsel, ymax, str(el), ha='left',va='center', 
    #             color='b', weight='bold')

    # ax.text(0.5, 0.01, 'Test', color='red', 
    #     bbox=dict(facecolor='none', edgecolor='red'))

    ''' target elevation '''
    # ha=ax.contour(rans,beams,eles,
    #               levels=te,
    #               colors='r')
    # # ysel = da.sel(rans=xmax, eles=te)
    # # print(te)
    # ysel = beamhgt_stdrefraction(xmax, te[0], Ho)
    # ax.text(xmax, ysel, str(te[0]), ha='left',va='center', 
    #             color='r', weight='bold')
    # # plt.clabel(ha,fmt='%1.1f')



    ''' filled area '''
    for e in te:
        ax.plot(da.range, da.sel(elev=e), color='r')
        telev = np.array([e]*len(ranges))
        y_top= map(beamhgt_stdrefraction, ranges, telev + (beam_width/2.), 
                    [Ho]*len(ranges))
        y_bot= map(beamhgt_stdrefraction, ranges, telev - (beam_width/2.), 
                    [Ho]*len(ranges))
        y_top = np.array(y_top)
        y_bot = np.array(y_bot)
        ax.fill_between(ranges, y_top, y_bot, where=y_top >= y_bot, 
                        facecolor='green', alpha =0.5)

    ax.set_ylim([0, ymax])
    ax.set_xlim([0, xmax])

    # ax.set_xticks(np.arange(0, 100, 10))
    # ax.set_yticks(np.arange(0, 12, 0.5))

    ax.set_xlabel('range [km]')
    ax.set_ylabel('beam height AGL [km]')
    plt.suptitle('Beam width: {}deg'.format(beam_width))
    plt.grid(True)
    plt.show()

    # S = pd.Series(H_target,index=ranges)
    # return S

def beamhgt_stdrefraction(r, el, Ho):
    ' From Rinehart p. 62'

    ER = 6371  # [km] Earth Radius
    R = (4 / 3.) * ER
    # Ho = 0  # [km] radar's altitude
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

if __name__ == 'main':
    main(sys.argv)
