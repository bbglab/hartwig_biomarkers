# hartwig_biomarkers

## Goal of Repository
* Clean and organize the Hartwig data request files into a single dataframe. 

![Overview](overview.pdf)

## Organization
* For each molecular file type, a pipeline computes features across all samples. 
* Output from each pipeline are then joined by their sample ids.
* Helper files to compute features for each molecular file type (*helper*) are located in mission_control folder.  

## Prerequisites to Run

### Approvals
* Need approval to use the Hartwig database: https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/ 
* Need the output from PURPLE, Isofox, and clinical data files stored on cluster. 

### Source and reference data 
* Source data is Hartwig data request files shared on August 9, 2022 (possible issues with other versions of the data request)
* Source file locations need to be specified in mission_control/treasure_map(.py,.R).

### Conda environments
* Stored in to conda_env folder

### QMap tool
* Use the QMap tool from bbglab to run jobs: https://github.com/bbglab/qmap

## Run the pipeline
* From the root directory:
```
$ python run.py

```
