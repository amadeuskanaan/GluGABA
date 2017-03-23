__author__ = 'kanaan' 'March 21 2017'


import os
import shutil
import subprocess
from utils.utils import mkdir_path


def fit_gaba(twxdir, voxel_name):
    lcmdir = mkdir_path(os.path.join(twxdir, 'lcmodel'))
    metdir = mkdir_path(os.path.join(twxdir, 'lcmodel', 'met'))
    h2odir = mkdir_path(os.path.join(twxdir, 'lcmodel', 'h2o'))

    shutil.copy(os.path.join(twxdir, voxel_name,  '%s_diff_lcm'%voxel_name), os.path.join(metdir, 'RAW'))
    # shutil.copy(os.path.join(twxdir, '%s_w'%voxel_name , '%s_w_lcm'%voxel_name), os.path.join(h2odir, 'RAW'))

    met = os.path.join(metdir, 'RAW')
    h2o = os.path.join(h2odir, 'RAW')


    hdr = [line.rstrip('\n') for line in open(os.path.join(twxdir, voxel_name,  '%s_diff_lcm'%voxel_name), 'r')][0:12]
    print hdr
    echot  = [hdr[hdr.index(item)] for item in hdr if 'echot' in item ][0][8:]
    hzpppm = [hdr[hdr.index(item)] for item in hdr if 'hzpppm' in item ][0][9:]
    nunfil = [hdr[hdr.index(item)] for item in hdr if 'NumberOfPoints' in item ][0][17:]
    deltat = [hdr[hdr.index(item)] for item in hdr if 'dwellTime=' in item ][0][12:]
    ppmst  = 4.2
    ppmend = 1.95


    file = open(os.path.join(lcmdir, 'control'), "w")
    file.write(" $LCMODL\n")
    file.write(" title= 'TWIX - %s' \n" %voxel_name)
    file.write(" srcraw= '%s' \n" % met)
    # file.write(" srch2o= '%s' \n" % h2o)
    file.write(" savdir= '%s' \n" % lcmdir)
    file.write(" ppmst= %s \n"%ppmst )
    file.write(" ppmend= %s\n"%ppmend)
    file.write(" nunfil= %s\n" % nunfil)
    file.write(" ltable= 7\n")
    file.write(" lps= 8\n")
    file.write(" lprint= 6\n")
    file.write(" lcsv= 11\n")
    file.write(" lcoraw= 10\n")
    file.write(" lcoord= 9\n")
    file.write(" hzpppm= %s\n" % hzpppm)
    file.write(" filtab= '%s/table'\n" % lcmdir)
    file.write(" filraw= '%s/met/RAW'\n" % lcmdir)
    file.write(" filps= '%s/ps'\n" % lcmdir)
    file.write(" filpri= '%s/print'\n" % lcmdir)
    file.write(" filh2o= '%s/h2o/RAW'\n" % lcmdir)
    file.write(" filcsv= '%s/spreadsheet.csv'\n" % lcmdir)
    file.write(" filcor= '%s/coraw'\n" % lcmdir)
    file.write(" filcoo= '%s/coord'\n" % lcmdir)
    file.write(" filbas= '/home/raid3/kanaan/.lcmodel/basis-sets/mega-press-3t-1.basis'\n")
    file.write(" echot= %s \n" % echot)
    file.write(" dows= F \n")
    file.write(" NEACH= 999 \n")  # export met fits
    file.write(" doecc= T\n")
    file.write(" deltat= %s\n" % deltat)
    file.write(" sptype= mega-press-3")
    file.write(" $END\n")
    file.close()


    lcm_command = ['/bin/sh', '/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdfv3', '%s' % lcmdir, '30', '%s' % lcmdir, '%s' % lcmdir]
    print subprocess.list2cmdline(lcm_command)
    subprocess.call(lcm_command)




twxdir     = '/scr/sambesi1/tmp/FIT_GABA/ASK/WCBT170321/twix/ACC'
voxel_name = 'ACC'

fit_gaba(twxdir, voxel_name)
