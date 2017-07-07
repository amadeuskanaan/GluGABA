import os
import shutil
from glob import glob
from variables import *
from utils.utils import mkdir_path


def check_spectra(population, workspace_dir, afs_dir, study_id, voxel_name):

    for subject in population:

        # Input/outut dirs
        subject_afs = os.path.join(afs_dir, subject, study_id)
        subject_dir = mkdir_path(os.path.join(workspace_dir, subject))


        #for svs_type in ['TWIX', 'RDA']:

        met_dir  = mkdir_path(os.path.join(subject_dir, 'SVS_TWIX', voxel_name))
        h20_dir  = mkdir_path(os.path.join(subject_dir, 'SVS_TWIX', '%s_w'%voxel_name))

        shutil.copy(glob('%s/*' %os.path.join(subject_afs, 'SVS', voxel_name, 'TWIX', voxel_name), met_dir))
        shutil.copy(glob('%s/*' %os.path.join(subject_afs, 'SVS', voxel_name, 'TWIX', '%s_w'%voxel_name), h20_dir))

        # copy svs data to local dir

check_spectra(['BTBT'], ssri_workspace, afs_dir, 'day1', 'ACC')





