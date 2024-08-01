#!/bin/bash
#SBATCH --no-requeue
set -e

source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step1_20231207/execution.env"
if [ -f "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step1_20231207/0.env" ]; then
	source "/workspace/projects/hartwig/biomarkers/repo/hartwig_biomarkers/launch_pad/step1_20231207/0.env"
fi

python $PWD/engine1/0_get-clinical.py

