#!/usr/bin/env python3
import argparse
import os
import subprocess
from bids.grabbids import BIDSLayout

__version__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'version')).read()

def run(command, env={}):
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=True,
                               env=merged_env)
    while True:
        line = process.stdout.readline()
        line = str(line, 'utf-8')[:-1]
        print(line)
        if line == '' and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d"%process.returncode)

stages_dict = {"brain_extraction": "1",
               "template_registration": "2",
               "tissue_segmentation": "3",
               "template_registration": "4",
               "cortical_thickness": "5",
               "qc": "6"}

parser = argparse.ArgumentParser(description='Cortical thickness estimation using ANTs.')
parser.add_argument('bids_dir', help='The directory with the input dataset '
                    'formatted according to the BIDS standard.')
parser.add_argument('output_dir', help='The directory where the output files '
                    'should be stored. If you are running group level analysis '
                    'this folder should be prepopulated with the results of the'
                    'participant level analysis.')
parser.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                    'Multiple participant level analyses can be run independently '
                    '(in parallel) using the same output_dir.',
                    choices=['participant'])
parser.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                   'corresponds to sub-<participant_label> from the BIDS spec '
                   '(so it does not include "sub-"). If this parameter is not '
                   'provided all subjects should be analyzed. Multiple '
                   'participants can be specified with a space separated list.',
                   nargs="+")
parser.add_argument('--n_cpus', help='Number of CPUs/cores available to use.',
                   default=1, type=int)
parser.add_argument('--stage', help='Which stage of ACT to run',
                    choices=stages_dict.keys())
parser.add_argument('-v', '--version', action='version',
                    version='BIDS-App example version {}'.format(__version__))


args = parser.parse_args()

run('bids-validator %s'%args.bids_dir)

layout = BIDSLayout(args.bids_dir)

subjects_to_analyze = []
# only for a subset of subjects
if args.participant_label:
    subjects_to_analyze = args.participant_label
# for all subjects
else:
    subjects_to_analyze = layout.get_subjects()

template_dir = "/opt/MICCAI2012-Multi-Atlas-Challenge-Data/"

template_dict = {"template_full": os.path.join(template_dir,
                                               "T_template0.nii.gz"),
                 "template_skullstripped": os.path.join(template_dir,
                                                        "T_template0_BrainCerebellum.nii.gz"),
                 "probability_mask": os.path.join(template_dir,
                                                  "T_template0_BrainCerebellumProbabilityMask.nii.gz"),
                 "registration_mask": os.path.join(template_dir,
                                                   "T_template0_BrainCerebellumRegistrationMask.nii.gz"),
                 "priors": os.path.join(template_dir,
                                        "Priors2/priors%d.nii.gz")}

# running participant level
if args.analysis_level == "participant":

    # find all T1s and skullstrip them
    for subject_label in subjects_to_analyze:
        T1w_files = layout.get(subject=subject_label, type='T1w',
                               extensions=['.nii','.nii.gz'],
                               return_type='file')
        if len(T1w_files) == 1:
            params = {"out_prefix": os.path.join(args.output_dir,
                                                 "sub-" + str(subject_label),
                                                 os.path.split(T1w_files[0])[-1].split('.')[0] + "_"),
                      "t1w": T1w_files[0]}
            params.update(template_dict)
            cmd = "antsCorticalThickness.sh " \
                  "-d 3 " \
                  "-a {t1w} " \
                  "-o {out_prefix} " \
                  "-e {template_full} " \
                  "-t {template_skullstripped} " \
                  "-m {probability_mask} " \
                  "-f {registration_mask} " \
                  "-p {priors}".format(**params)

            if args.stage:
                cmd += " -y " + stages_dict[args.stage]

            print(cmd)
            run(cmd, env={'ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS': str(args.n_cpus)})
