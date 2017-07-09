import os
import subprocess
from variables import *
from utils.utils import mkdir_path



def run_frequency_phase_correction(population, workspace_dir, study_id, voxel_name, svs_type):

    for subject in population:


        subject_dir = mkdir_path(os.path.join(workspace_dir, subject, study_id))

        twx_dir     = os.path.join(subject_dir, 'SVS', voxel_name, 'TWIX')
        lcm_dir     = mkdir_path(os.path.join(subject_dir, 'LCMODEL', voxel_name, 'TWIX'))

        # Run frequency and phase drift correction
        os.chdir(twx_dir)

        if svs_type == 'PRESS':
            preproc = ['matlab', '-nodesktop', '-nosplash', '-noFigureWindows',
                        '-r "run_pressproc_auto.m(\'%s\') ; quit;"'%voxel_name]

        elif svs_type == 'MEGA_PRESS':
            preproc = ['matlab', '-nodesktop', '-nosplash', '-noFigureWindows',
                       '-r "run_megapressproc_auto.m.m(\'%s\') ; quit;"' % voxel_name]

        #if not os.path.isfile(os.path.join(twx_xdir, voxel_name, voxel_name, '%s_diff_lcm' %voxel_name)):
        #    print ' Running Frequnency and Phase drift correction for %s' %voxel_name
        subprocess.call(preproc)

run_frequency_phase_correction(['BTBT'], ssri_workspace, 'day1', 'ACC', 'PRESS')

