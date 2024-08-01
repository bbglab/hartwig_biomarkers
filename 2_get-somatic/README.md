# 2_get-somatic

## get_somatic-features

#### Purpose

* Compute somatic mutational features across all sampleIds in Hartwig. 

#### Inputs

* somatic file paths output from 1_create-file-index 
* reference file: contains encode genes 
* helper file: mission_control/somatic_help.py

## Output
* A large dataframe, each row corresponds to a sampleId, columns are somatic mutational features. 

## Issues
* Repo currently takes > 2 days to run across Hartwig. Should be able parallelize feature gathering. 
