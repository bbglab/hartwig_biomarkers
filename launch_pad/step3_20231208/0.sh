#!/bin/bash
#SBATCH --no-requeue
set -e

source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step3_20231208/execution.env"
if [ -f "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step3_20231208/0.env" ]; then
	source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step3_20231208/0.env"
fi

. "/home/$USER/anaconda3/etc/profile.d/conda.sh"
conda activate r_env
Rscript $PWD/engine3/1_get-clinical.r

