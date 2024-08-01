# hartwig_biomarkers

## Goal
* Clean and organize the Hartwig data request files into a single dataframe for statistical analyses. 

![Overview](overview.pdf)

## Organization
* For each molecular file type, a pipeline computes features across all samples. 
* Output from each pipeline are then joined by their sample ids.
* Helper files to compute features for each molecular file type (*helper*) are located in mission_control folder.  

## Prerequisites

#### Source data
* Source data is Hartwig data request files shared on August 9, 2022. 
** Use output from PURPLE, Isofox, and clinical data files.
* Source file locations are specified in mission_control/treasure_map(.py,.R).
* The code makes use of reference files stored here: /workspace/datasets/hartwig/20211021/biomarkers/ref/

#### Conda Environments

I use 2 conda environments when running the code. 

* An python environment to run the scripts store in ~/launch_pad/(engine1)(engine2)
* An R environment to run the scripts store in ~/launch_pad/(engine3)(engine4)

## Run the pipeline
* From the root directory:
```
$ python run.py
```
