import os
import subprocess
import shutil
from variables import *
from utils.utils import mkdir_path



def run_frequency_phase_correction(population, workspace_dir, study_id, voxel_name, svs_type):

    for subject in population:


        subject_dir = os.path.join(workspace_dir, subject, study_id)
        twx_dir     = os.path.join(subject_dir, 'SVS', voxel_name, 'TWIX')
        lcm_dir     = mkdir_path(os.path.join(subject_dir, 'LCMODEL', voxel_name, 'TWIX'))
        met_dir     = mkdir_path(os.path.join(lcm_dir, 'met'))
        h2o_dir     = mkdir_path(os.path.join(lcm_dir, 'h2o'))

        def make_press_control_file(lcmodel_dir, met, h2o, title, ppmst, ppmend):

            hdr = [line.rstrip('\n') for line in open(met, 'r')][0:12]
            print hdr
            echot = [hdr[hdr.index(item)] for item in hdr if 'echot' in item][0][8:]
            hzpppm = [hdr[hdr.index(item)] for item in hdr if 'hzpppm' in item][0][9:]
            nunfil = [hdr[hdr.index(item)] for item in hdr if 'NumberOfPoints' in item][0][17:]
            deltat = [hdr[hdr.index(item)] for item in hdr if 'dwellTime=' in item][0][12:]

            '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                              Building the control file
            '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            print '...building control file'
            file = open(os.path.join(lcmodel_dir, 'contro,l'), "w")
            file.write(" $LCMODL\n")
            file.write(" title= 'TWIX - %s' \n" % title)
            file.write(" srcraw= '%s' \n" % met)
            file.write(" srch2o= '%s' \n" % h2o)
            file.write(" savdir= '%s' \n" % lcmodel_dir)
            file.write(" ppmst= %s \n" % ppmst)
            file.write(" ppmend= 0.3\n")
            file.write(" nunfil= %s\n" % nunfil)
            file.write(" ltable= 7\n")
            file.write(" lps= 8\n")
            file.write(" lprint= 6\n")
            file.write(" lcsv= 11\n")
            file.write(" lcoraw= 10\n")
            file.write(" lcoord= 9\n")
            file.write(" hzpppm= %s\n" % hzpppm)
            file.write(" filtab= '%s/table'\n" % lcmodel_dir)
            file.write(" filraw= '%s/met/RAW'\n" % lcmodel_dir)
            file.write(" filps= '%s/ps'\n" % lcmodel_dir)
            file.write(" filpri= '%s/print'\n" % lcmodel_dir)
            file.write(" filh2o= '%s/h2o/RAW'\n" % lcmodel_dir)
            file.write(" filcsv= '%s/spreadsheet.csv'\n" % lcmodel_dir)
            file.write(" filcor= '%s/coraw'\n" % lcmodel_dir)
            file.write(" filcoo= '%s/coord'\n" % lcmodel_dir)
            file.write(" filbas= '/home/raid3/kanaan/.lcmodel/basis-sets/press_te30_3t_01a.basis'\n")
            file.write(" echot= %s \n" % echot)
            file.write(" dows= T \n")
            # file.write(" NEACH= 999 \n") # export met fits
            # file.write(" DEGPPM =0 \n")
            file.write(" doecc= T\n")
            file.write(" deltat= %s\n" % deltat)
            file.write(" $END\n")
            file.close()

            lcm_command = ['/bin/sh', '/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdfv3', '%s' % lcmodel_dir,
                           '30', '%s' % lcmodel_dir, '%s' % lcmodel_dir]
            print subprocess.list2cmdline(lcm_command)
            subprocess.call(lcm_command)

        def make_megapress_control_file(lcmodel_dir, met, h2o, title, ppmst, ppmend):

            hdr = [line.rstrip('\n') for line in open(met, 'r')][0:12]
            print hdr
            echot = [hdr[hdr.index(item)] for item in hdr if 'echot' in item][0][8:]
            hzpppm = [hdr[hdr.index(item)] for item in hdr if 'hzpppm' in item][0][9:]
            nunfil = [hdr[hdr.index(item)] for item in hdr if 'NumberOfPoints' in item][0][17:]
            deltat = [hdr[hdr.index(item)] for item in hdr if 'dwellTime=' in item][0][12:]

            file = open(os.path.join(lcmodel_dir, 'control'), "w")
            file.write(" $LCMODL\n")
            file.write(" title= 'TWIX - %s' \n" % voxel_name)
            file.write(" srcraw= '%s' \n" % met)
            file.write(" srch2o= '%s' \n" % h2o)
            file.write(" savdir= '%s' \n" % lcmodel_dir)
            file.write(" ppmst= %s \n" % ppmst)
            file.write(" ppmend= %s\n" % ppmend)
            file.write(" nunfil= %s\n" % nunfil)
            file.write(" ltable= 7\n")
            file.write(" lps= 8\n")
            file.write(" lprint= 6\n")
            file.write(" lcsv= 11\n")
            file.write(" lcoraw= 10\n")
            file.write(" lcoord= 9\n")
            file.write(" hzpppm= %s\n" % hzpppm)
            file.write(" filtab= '%s/table'\n" % lcmodel_dir)
            file.write(" filraw= '%s/met/RAW'\n" % lcmodel_dir)
            file.write(" filps= '%s/ps'\n" % lcmodel_dir)
            file.write(" filpri= '%s/print'\n" % lcmodel_dir)
            file.write(" filh2o= '%s/h2o/RAW'\n" % lcmodel_dir)
            file.write(" filcsv= '%s/spreadsheet.csv'\n" % lcmodel_dir)
            file.write(" filcor= '%s/coraw'\n" % lcmodel_dir)
            file.write(" filcoo= '%s/coord'\n" % lcmodel_dir)
            file.write(" filbas= '/home/raid3/kanaan/.lcmodel/basis-sets/mega-press-3t-1.basis'\n")
            file.write(" echot= %s \n" % echot)
            file.write(" dows= T \n")
            #file.write(" NEACH= 999 \n")  # export met fits
            file.write(" doecc= T\n")
            file.write(" deltat= %s\n" % deltat)
            file.write(" sptype= mega-press-3")
            file.write(" $END\n")
            file.close()

            lcm_command = ['/bin/sh', '/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdfv3', '%s' % lcmodel_dir,
                           '30', '%s' % lcmodel_dir, '%s' % lcmodel_dir]
            print subprocess.list2cmdline(lcm_command)
            subprocess.call(lcm_command)


        if svs_type == 'PRESS':

            shutil.copy(os.path.join(twx_dir, voxel_name, '%s_lcm' % voxel_name), os.path.join(met_dir, 'RAW'))
            shutil.copy(os.path.join(twx_dir, '%s_w' % voxel_name, '%s_w_lcm' % voxel_name), os.path.join(h2o_dir, 'RAW'))
            met = os.path.join(met_dir, 'RAW')
            h2o = os.path.join(h2o_dir, 'RAW')
            make_press_control_file(lcm_dir, met, h2o, '%s - %s' % (subject, voxel_name), 4.0, 0)

        elif svs_type == 'MEGA_PRESS':
            shutil.copy(os.path.join(twx_dir, voxel_name, '%s_diff_lcm' % voxel_name), os.path.join(met_dir, 'RAW'))
            shutil.copy(os.path.join(twx_dir, '%s_w' % voxel_name, '%s_w_lcm' % voxel_name), os.path.join(h2o_dir, 'RAW'))
            met = os.path.join(met_dir, 'RAW')
            h2o = os.path.join(h2o_dir, 'RAW')



run_frequency_phase_correction(['BTBT'], ssri_workspace, 'day1', 'ACC', 'PRESS')


