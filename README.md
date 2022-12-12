## BIDS App for calculating cortical thickness using ANTs

This BIDS App runs ANTs cortical thickness estimation pipeline.

For more information about the specification of BIDS Apps see [here](https://docs.google.com/document/d/1E1Wi5ONvOVVnGhj21S1bmJJ4kyHFT7tkxnV3C23sjIE/edit#).

### Description
The app finds all T1w files for each subject and runs antsCorticalThickness.sh (if there is only one T1w file per subject) or 
antsLongitudinalCorticalThickness.sh (if there are more than one T1w files).

### Documentation
https://github.com/ANTsX/ANTs

### How to report errors
https://github.com/BIDS-Apps/antsCorticalThickness/issues

### Acknowledgements
https://github.com/ANTsX/ANTs#boilerplate-ants

### Usage
This App has the following command line arguments:

		usage: run.py [-h]
                  [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                  [--n_cpus N_CPUS]
                  [--stage {brain_extraction,template_registration,tissue_segmentation,qc,cortical_thickness}]
                  [-v]
                  bids_dir output_dir {participant}

    Cortical thickness estimation using ANTs.

    positional arguments:
      bids_dir              The directory with the input dataset formatted
                            according to the BIDS standard.
      output_dir            The directory where the output files should be stored.
                            If you are running group level analysis this folder
                            should be prepopulated with the results of
                            theparticipant level analysis.
      {participant}         Level of the analysis that will be performed. Multiple
                            participant level analyses can be run independently
                            (in parallel) using the same output_dir.

    optional arguments:
      -h, --help            show this help message and exit
      --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                            The label(s) of the participant(s) that should be
                            analyzed. The label corresponds to
                            sub-<participant_label> from the BIDS spec (so it does
                            not include "sub-"). If this parameter is not provided
                            all subjects should be analyzed. Multiple participants
                            can be specified with a space separated list.
      --n_cpus N_CPUS       Number of CPUs/cores available to use.
      --stage {brain_extraction,template_registration,tissue_segmentation,qc,cortical_thickness}
                            Which stage of ACT to run
      -v, --version         show program's version number and exit

To run it in participant level mode (for one participant):

    docker run -i --rm \
		-v /Users/filo/data/ds005:/bids_dataset:ro \
		-v /Users/filo/outputs:/outputs \
		bids/antscorticalthickness \
		/bids_dataset /outputs participant --participant_label 01
