import os
from utils.utils import *
from variables import *
import subprocess


def lcmodel_rda(population, workspace_dir, study_day, voxel_name, sequence):


    for subject in population:

        #I/O
        subject_dir = os.path.join(workspace_dir, subject, study_day)
        os.system('chmod -R 750 * ')
        met = os.path.join(subject_dir, 'SVS', voxel_name, 'RDA', voxel_name, '%s.rda'%voxel_name)
        h2o = os.path.join(subject_dir, 'SVS', voxel_name, 'RDA', '%s_w'%voxel_name, '%s_w.rda'%voxel_name)

        lcmodel_dir = mkdir_path(os.path.join(subject_dir, 'LCMODEL_RDA', voxel_name))
        met_raw     = mkdir_path(os.path.join(lcmodel_dir, 'met'))
        h2o_raw     = mkdir_path(os.path.join(lcmodel_dir, 'h2o'))

        # Run lcmodel bin2raw
        # if not os.path.isfile(os.path.join(h2o_raw, 'RAW')):
        #     os.system('/home/raid3/kanaan/.lcmodel/siemens/bin2raw %s %s met'%(met, lcmodel_dir))
        #     os.system('/home/raid3/kanaan/.lcmodel/siemens/bin2raw %s %s h2o'%(h2o, lcmodel_dir))

lcmodel_rda(['KA3X'], ssri_workspace, 'day1', 'ACC', 'PRESS')
