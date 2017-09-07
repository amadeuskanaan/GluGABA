import os
import shutil
import glob
from variables import *
from utils.utils import mkdir_path
import shutil

def check_spectra(population, workspace_dir, afs_dir, study_day, voxel_name, sequence):

    for subject in population:

        # Input/outut dirs
        subject_afs = os.path.join(afs_dir, subject, study_day)
        subject_dir = mkdir_path(os.path.join(workspace_dir, subject, study_day))

        if sequence is 'PRESS':
            seq = 'se'
        elif sequence is 'MEGA_PRESS':
            seq = 'mp'


        ########## for svs_type in ['TWIX', 'RDA']:


        twx_met_src = glob.glob(os.path.join(subject_afs, 'SVS', voxel_name, 'TWIX', voxel_name, '*'))[0]
        twx_h2o_src = glob.glob(os.path.join(subject_afs, 'SVS', voxel_name, 'TWIX', '%s_w'%voxel_name, '*'))[0]

        print twx_met_src
        print twx_h2o_src

        # twx_met_dir  = mkdir_path(os.path.join(subject_dir, 'SVS', voxel_name, 'TWIX',  voxel_name))
        # twx_h20_dir  = mkdir_path(os.path.join(subject_dir, 'SVS', voxel_name, 'TWIX', '%s_w'%voxel_name))
        #
        # os.system('cp %s %s ' % (twx_met_dir, twx_met_file))


        # rda_met_dir  = mkdir_path(os.path.join(subject_dir, 'SVS', voxel_name, 'RDA',  voxel_name))
        # rda_h20_dir  = mkdir_path(os.path.join(subject_dir, 'SVS', voxel_name, 'RDA', '%s_w'%voxel_name))


        # rda_met_file = glob.glob(os.path.join(subject_afs, 'SVS', voxel_name, 'RDA', '%s%s.rda'%(seq,voxel_name)))[0]
        # rda_h20_file = glob.glob(os.path.join(subject_afs, 'SVS', voxel_name, 'RDA', '%s%sref.rda'%(seq,voxel_name)))[0]

        # copy svs data to local dir
        # os.system('cp %s %s '%(twx_met_dir, twx_met_file))
        # os.system('cp %s %s '%(twx_h20_dir, twx_h20_file))
        #
        # os.system('cp %s %s ' % (rda_met_dir, rda_met_file))
        # os.system('cp %s %s ' % (rda_h20_dir, rda_h20_file))

check_spectra(['KA3X'], ssri_workspace, afs_dir, 'day1', 'ACC', 'PRESS')
check_spectra(['KA3X'], ssri_workspace, afs_dir, 'day1', 'M1', 'PRESS')
check_spectra(['KA3X'], ssri_workspace, afs_dir, 'day1', 'M1m', 'MEGA_PRESS')
