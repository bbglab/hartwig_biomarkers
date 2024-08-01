# hartwig_biomarkers

![pipeline_overview](overview.pdf)

## Content

* Repo contains code to create a biomarkers dataset from hartwig (large dataframe that consolidates features of different type). 
* For each molecular data type, a separate pipeline computes features. 
* Features computed from each individual pipeline are joined into a dataframe and output. 

## Prerequisites

#### Source data
* Currently, all the inputs to the repo are hard-coded and placed in the file mission_control/treasure_map(.py,.R).
* The raw source data is stored on our cluster in the folder: /workspace/datasets/hartwig/20211021/
* The code makes use of reference files stored here: /workspace/datasets/hartwig/20211021/biomarkers/ref/
* File paths must be pre-specified in the treasure_map.py(.R) in the mission_control folder. 

#### Conda Environments

I use 2 conda environments when running the code. 

* An python environment to run the scripts store in ~/launch_pad/(engine1)(engine2)
* An R environment to run the scripts store in ~/launch_pad/(engine3)(engine4)

## Running the pipeline
* All code run in the pipeline is initially created in notebooks. To run the pipeline, first convert them to scripts:
```
$ python launch_pad/prepare_the_engines.py
```
* Then the pipeline should be run from in the launch_pad folder: 
```
cd launch_pd
./go.sh 
```

### Issues
* Inputs in mission_control/treasure_map.* are hard-coded.
* File paths in qmaps jobs are hard-coded. 
* get_somatic-features.py takes >50 hours to run, could be parallelized.
* Needs code review and more QA.
* Need help to share conda environments, test if others can run the pipeline.  
