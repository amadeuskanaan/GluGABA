__author__ = 'kanaan' 'March 21 2017'


import os
import shutil
import subprocess
import dicom as pydicom
from utils.utils import mkdir_path
import nipype.interfaces.spm.utils as spmu
from utils.utils import mkdir_path, find_cut_coords
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm, inch, pica
import nibabel as nb

workspace_dir = '/scr/sambesi1/MEGA_PRESS/'

def make_svs_anatomical(population, workspace, voxel_name):

    for subject in population:

        subject_dir = os.path.join(workspace, subject)
        dicom_dir   = os.path.join(subject_dir, 'DICOM')
        svs_dir     = os.path.join(subject_dir, 'SVS')
        nifti_dir   = mkdir_path(os.path.join(subject_dir, 'NIFTI'))

        ########## Get MP2RAGE UNI
        if not os.path.isfile( os.path.join(nifti_dir, 'ANATOMICAL.nii')):
            print 'Converting MP2RAGE '

            dicoms = [os.path.join(dicom_dir, dicom) for dicom in os.listdir(dicom_dir)]
            T1_list = []

            for dicom in dicoms:
                try:

                    dcm_read = pydicom.read_file(dicom, force=True)
                    sequence = dcm_read.SeriesDescription
                except AttributeError:
                    continue

                if 'mp2rage_p3_602B_UNI_Images' in sequence:
                    T1_list.append(dicom)

            # convert T1 anatomical to NIFTI with SPM
            print 'Converting Dicom to Nifti for %s' % subject
            spm_dicom_convert = spmu.DicomImport()
            spm_dicom_convert.inputs.format = 'nii'
            spm_dicom_convert.inputs.in_files = T1_list
            spm_dicom_convert.inputs.output_dir = nifti_dir
            spm_dicom_convert.run()

            # rename output file
            os.system('mv %s/*nii %s/ANATOMICAL.nii' %(nifti_dir, nifti_dir))


        # make svs mask
        rda =[]
        if not os.path.isfile(os.path.join(svs_dir, voxel_name, 'RDA', '.nii')):
            for root, dirs, files, in os.walk(os.path.join(svs_dir, voxel_name, 'RDA'), topdown=False):
                for name in files:
                    if 'supp' in name and 'edit1' in name:
                        rda.append(os.path.join(name))

            if rda is []:
                print 'RDA metabolite data does not exist for subject %s' % subject


            T1Path = os.path.join(subject_dir, 'NIFTI' + '/')
            T1Image = 'ANATOMICAL.nii'
            svs_path = os.path.join(svs_dir, voxel_name, 'RDA' + '/')
            svs_file = rda[0]

            matlab_command = ['matlab', '--version', '8.2', '-nodesktop', '-nosplash', '-nojvm',
                              '-r "RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;"'
                              % (T1Path, T1Image, svs_path, svs_file)]
            subprocess.call(matlab_command)

            os.system('mv %s/*Mask.nii %s' % (nifti_dir, os.path.join(svs_dir, voxel_name, 'RDA')))
            os.system('mv %s/*coord.txt %s' % (nifti_dir, os.path.join(svs_dir, voxel_name, 'RDA')))



def run_frequency_phase_correction(population, workspace, voxel_name):

    for subject in population:

        twxdir = os.path.join(workspace_dir, subject, 'SVS', voxel_name, 'TWIX')


        # Run frequency and phase drift correction
        os.chdir(twxdir)
        preproc_acc = ['matlab', '-nodesktop', '-nosplash', '-noFigureWindows',
                       '-r "run_megapressproc_auto(\'%s\') ; quit;"'%voxel_name]

        if not os.path.isfile(os.path.join(twxdir, voxel_name, voxel_name, '%s_diff_lcm' %voxel_name)):
            print ' Running Frequnency and Phase drift correction for %s' %voxel_name
            subprocess.call(preproc_acc)



def lcmodel_gaba(population, workspace, voxel_name, water = True):


    for subject in population:

        twxdir = os.path.join(workspace_dir, subject, 'SVS', voxel_name, 'TWIX')
        lcmdir = mkdir_path(os.path.join(twxdir, 'lcmodel'))
        metdir = mkdir_path(os.path.join(twxdir, 'lcmodel', 'met'))
        h2odir = mkdir_path(os.path.join(twxdir, 'lcmodel', 'h2o'))


        shutil.copy(os.path.join(twxdir, voxel_name,  '%s_diff_lcm'%voxel_name), os.path.join(metdir, 'RAW'))
        met = os.path.join(metdir, 'RAW')

        if water:
            shutil.copy(os.path.join(twxdir, '%s_w'%voxel_name , '%s_w_lcm'%voxel_name), os.path.join(h2odir, 'RAW'))
            h2o = os.path.join(h2odir, 'RAW')
            dow = 'T'

        else:
            dow = 'F'

        hdr = [line.rstrip('\n') for line in open(os.path.join(twxdir, voxel_name,  '%s_diff_lcm'%voxel_name), 'r')][0:12]
        print hdr
        print ''
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
        if water:
            file.write(" srch2o= '%s' \n" % h2o)
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
        file.write(" dows= %s \n" %dow)

        file.write(" NEACH= 999 \n")  # export met fits
        file.write(" doecc= T\n")
        file.write(" deltat= %s\n" % deltat)
        file.write(" sptype= mega-press-3")
        file.write(" $END\n")
        file.close()

        lcm_command = ['/bin/sh', '/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdfv3', '%s' % lcmdir, '30', '%s' % lcmdir, '%s' % lcmdir]
        print subprocess.list2cmdline(lcm_command)
        subprocess.call(lcm_command)


def make_report(population, workspace, voxel_name):

    for subject in population:
        subdir = os.path.join(workspace_dir, subject)
        rdadir = os.path.join(subdir, 'SVS', voxel_name, 'RDA')
        twxdir = os.path.join(subdir, 'SVS', voxel_name, 'TWIX')
        lcmdir = mkdir_path(os.path.join(twxdir, 'lcmodel'))

        rda = []
        for root, dirs, files, in os.walk(rdadir, topdown=False):
            for name in files:
                if 'supp' in name and 'edit1' in name:
                    rda.append(os.path.join(rdadir, name))

        reader = open(rda[0], 'r')
        for line in reader:
            if 'SeriesDescription' in line:
                Series = line[19:30]
            elif 'TR:' in line:
                TR = line[4:8]
            elif 'TE:' in line:
                TE = line[4:6]
            elif 'VectorSize' in line:
                nfil = line[12:16]
            elif 'NumberOfAverages' in line:
                NS = line[18:21]
            elif 'PatientSex' in line:
                Sex = line[12:13]
            elif 'PatientAge' in line:  #
                Age = line[13:15]
            elif 'PixelSpacingRow' in line:
                PSR = float(line[17:19])
            elif 'PixelSpacingCol' in line:
                PSC = float(line[17:20])
            elif 'PixelSpacing3D:' in line:
                PS3d = float(line[16:19])
            elif 'StudyDate' in line:
                datex = line[0:19]



        lcm_plot = os.path.join(twxdir, '%s_lcmodel-0.png' % voxel_name[0:3])

        if not os.path.isfile(lcm_plot):
            lcmodel = os.path.join(twxdir, 'lcmodel', 'ps.pdf')

            make_png = ['convert', '-density', '300', '-trim', '%s' % lcmodel,# '-quality', '300', '-sharpen', '0x1.0',
                        '%s/%s_lcmodel.png' % (twxdir,voxel_name[0:3])]
            subprocess.call(make_png)


        #make report
        anat  = os.path.join(subdir, 'NIFTI', 'ANATOMICAL.nii')
        svs   = os.path.join(subdir, 'SVS', voxel_name,  'RDA/RDA_Mask.nii')

        # get data into matrix
        anat_load = nb.load(anat)
        svs_load = nb.load(svs)
        anat_data = anat_load.get_data()
        svs_data = svs_load.get_data()

        # get svs cut coords
        coords = np.round(find_cut_coords(svs_load))

        print coords

        # convert zeros to nans for visualization purposes
        svs_data[svs_data == 0] = np.nan

        # plot voxel on anat
        fig = plt.figure()
        fig.set_size_inches(6.5, 6.5)
        fig.subplots_adjust(wspace=0.005)
        # 1
        ax1 = plt.subplot2grid((1, 3), (0, 0), colspan=1, rowspan=1)
        ax1.imshow(anat_data[int(coords[0]), :, :], matplotlib.cm.bone_r)
        ax1.imshow(svs_data[int(coords[0]), :, :], matplotlib.cm.rainbow_r, alpha=0.7)
        ax1.set_xlim(23, 157)
        ax1.set_ylim(101, 230)
        ax1.axes.get_yaxis().set_visible(False)
        ax1.axes.get_xaxis().set_visible(False)
        # 2
        ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=1, rowspan=1)
        ax2.imshow(np.rot90(anat_data[:, :, int(coords[2])]), matplotlib.cm.bone_r)
        ax2.imshow(np.rot90(svs_data[:, :, int(coords[2])]), matplotlib.cm.rainbow_r, alpha=0.7)
        ax2.set_xlim(230, 20)
        ax2.set_ylim(207, 4)
        ax2.axes.get_yaxis().set_visible(False)
        ax2.axes.get_xaxis().set_visible(False)
        # 3
        ax3 = plt.subplot2grid((1, 3), (0, 2), colspan=1, rowspan=1)
        ax3.imshow(anat_data[:, int(coords[1]), :], matplotlib.cm.bone_r, origin='lower')
        ax3.imshow(svs_data[:, int(coords[1]), :], matplotlib.cm.rainbow_r, alpha=0.7, origin='lower')
        ax3.set_xlim(38, 140)
        ax3.set_ylim(160, 60)
        ax3.axes.get_yaxis().set_visible(False)
        ax3.axes.get_xaxis().set_visible(False)
        fig.tight_layout()
        fig.savefig('%s/localization_%s.png' % (twxdir, voxel_name), dpi=200, bbox_inches='tight')

        # create qc report
        report = canvas.Canvas(os.path.join(twxdir, 'QC_REPORT_%s.pdf' % voxel_name), pagesize=(1280, 1556))
        report.setFont("Helvetica", 40)
        report.drawImage(os.path.join(twxdir, 'localization_%s.png' % voxel_name), 1, inch * 13.5)
        report.drawImage(lcm_plot, 30, inch * 1, width=1200, height=800, mask='auto')
        report.setFont("Helvetica", 30)
        report.drawString(175, inch * 20, ' %s (%s-%s), TR=%s, TE=%s, NAV=%s ,Volume=%sx%sx%s'
                          % (subject, Age, Sex, TR, TE, NS, int(PSR), int(PSC), int(PS3d)))
        # report.showPage()
        report.save()


make_svs_anatomical(['ZS9T170327'], workspace_dir, 'M1')
run_frequency_phase_correction(['ZS9T170327'], workspace_dir, 'M1')
lcmodel_gaba(['ZS9T170327'], workspace_dir, 'M1')
make_report(['ZS9T170327'], workspace_dir, 'M1')
#