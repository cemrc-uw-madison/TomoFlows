#!/usr/bin/python3

import os
import argparse
import subprocess
from pathlib import Path

from scripts.program.mdoc import MDoc

class EERMotionOptions:
    gain = None
    pixelSize = None
    exposureDose = None

def convertTifMrc(in_tif, out_mrc):
    ''' Given an gain in tiff format convert to MRC '''
    if (os.path.exists(out_mrc)):
        print(out_mrc + ' output mrc already exists, will not convert tif')
    else: 
        command_prefix = '/bin/bash -c "source ${IMOD_DIR}/IMOD-linux.sh && '
        executable= 'tif2mrc'
        args = [executable, in_tif, out_mrc]
        subprocess.run(f'{command_prefix}{" ".join(args)}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

def readMdoc(mdoc_filename):
    # The 'mdoc' metadata provides information for the total dose and pixel size.
    if (os.path.exists(mdoc_filename)):
        print('Extracting parameters from : ' + mdoc_filename)
        opts = EERMotionOptions()
        eer_mdoc = MDoc.parse(mdoc_filename)
        if (eer_mdoc and len(eer_mdoc.framesets) > 0):
            frameDesc =  eer_mdoc.framesets[0]
            if 'PixelSpacing' in frameDesc.nameVal:
                opts.pixelSize = float(frameDesc.nameVal['PixelSpacing'])
            if 'GainReference' in frameDesc.nameVal:
                opts.gain = frameDesc.nameVal['GainReference']
            if 'ExposureDose' in frameDesc.nameVal:
                opts.exposureDose = frameDesc.nameVal['ExposureDose']
        return opts

    return None

def prepareIntFile(in_eer, total_dose, out_fmintfile):
    ''' Given an EER image, create an FmIntFile '''
    if (os.path.exists(out_fmintfile)):
        print(out_fmintfile + ' exists: skipping fmintfile')
        return 0

    print('Will create FmIntFile.txt at ' + str(out_fmintfile))    
    #  Use `header <image.eer>` to determine the number of 'sections'
    #  Need to find the line starting with and pull out an integer value from this line.
    match_str = ' Number of columns, rows, sections .....'  # after this are 3 integers, frames is the 3rd.
    frames = None
    command_prefix = '/bin/bash -c "source ${IMOD_DIR}/IMOD-linux.sh && '
    run_result = subprocess.run(f'{command_prefix}{" ".join(["header", in_eer])}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout = run_result.stdout
    lines = stdout.splitlines()
    for test in lines:
        if test.startswith(match_str):
            values = test.split(match_str)[1]
            numbers = values.split()
            frames = numbers[2]
    if frames:
        # Determine the dose per fraction as total_dose / fractions 
        dose_per = float(total_dose) / float(frames)

        # Dynamically scale the number of fractions so that e- dose per fraction > 0.01
        frames_per_fraction = 9
        dose_per_fraction = frames_per_fraction * dose_per
        while (dose_per_fraction < 0.1 and frames_per_fraction < int(frames)):
            frames_per_fraction += 9
            dose_per_fraction = float(frames_per_fraction * dose_per)

        # Determine the number of total fractions as frames / 9
        fractions = int(frames) / frames_per_fraction

        # Write out values of 'frames fractions dose_per' into our output file. 
        with open(out_fmintfile, 'w') as f:
            line = '{:d} {:d} {:.4f}\n'.format(int(frames), int(fractions), float(dose_per))
            f.write(line)
        return 0
    else: 
        print('ERROR: Unable to parse header output for frames.')
    return 1    

def motionCorrectEer(in_eer, fmIntFilePath, EEROpts, out_mrc):
    ''' Given EER and mdoc describing file do motion correction '''
    if (os.path.exists(out_mrc)):
        print(str(out_mrc) + ' exists: skipping motionCor')
    else:
        print(str(out_mrc) + ' will be created by motionCor...')

        motionCor = 'motioncor2'
        inputType = "-InEER"

        args = [motionCor, 
            inputType, str(in_eer), 
            "-OutMrc", str(out_mrc), 
            "-FtBin", "2",
            "-EerSampling", "2",
            "-Patch", "5 5", 
            "-Iter", "20", 
            "-Tol", "0.5", 
            "-Gpu", "0 1 2 3",
            "-Gain", str(EEROpts.gain),
            "--EerSampling", "2",
            "-PixSize", str(EEROpts.pixelSize / 2.0),
            "-FmIntFile", str(fmIntFilePath)]

        subprocess.call(args)

def main():
    # 1. Provide a command-line arguments
    parser = argparse.ArgumentParser(description='Motion-correct EER movies to MRC')
    parser.add_argument('--eer', help='input EER file', required=True)
    parser.add_argument('--out', help='output MRC file', required=True)
    parser.add_argument('--mdoc', help='input MDOC file', required=True)
    parser.add_argument('--dosefile', help='FmIntFile.txt for integrations in motionCor2', required=False, default=None)
    args = parser.parse_args()

    eer_file = args.eer
    mdoc_file = args.mdoc
    output_mrc = args.out

    # read the mdoc details
    EEROpts = readMdoc(mdoc_file)

    # create from the input file and mdoc if necessary
    dosefile = args.dosefile
    if not dosefile:
        path = Path(args.eer)
        folder = path.parent.absolute()
        dosefile = os.path.join(folder, 'FmIntfile.txt')
        prepareIntFile(args.eer, EEROpts.exposureDose, dosefile)

    # convert the gain from a .gain/tiff to .mrc format.
    parent_dir = Path(args.mdoc).parent
    gain_tiff = os.path.join(parent_dir, EEROpts.gain)
    gain_mrc = os.path.join(parent_dir, Path(gain_tiff).with_suffix('.mrc'))
    convertTifMrc(gain_tiff, gain_mrc)
    EEROpts.gain = gain_mrc

    # next, motion correct the images.
    motionCorrectEer(eer_file, dosefile, EEROpts, output_mrc)

if __name__ == "__main__":
    main()
