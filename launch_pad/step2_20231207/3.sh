#!/bin/bash
#SBATCH --no-requeue
set -e

source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step2_20231207/execution.env"
if [ -f "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step2_20231207/3.env" ]; then
	source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step2_20231207/3.env"
fi

. "/home/$USER/anaconda3/etc/profile.d/conda.sh"
conda activate base
python  $PWD/engine2/get-cnv-overall.py

