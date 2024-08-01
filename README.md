# Hartwig Biomarkers

## Goal of Repository
[Overview](overview.pdf)
* Clean and organize the Hartwig data request files into a single dataframe. 

## Organization
* For each file type, a pipeline computes and organizes features across all samples. 
* Output from each pipeline are then joined by their sample ids.

## Prerequisites to Run

### Hartwig Data Request Approval
* Harwtig data request: https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/ 
* PURPLE, ISOFOX, and clinical data output. 

### Source and reference data 
* Run and tested on Hartwig data request files shared on August 9, 2022.
* Source file locations need to be specified correctly in mission_control/treasure_map(.py,.R).

### QMap and conda environments
* Jobs are submitted with the QMap tool from the bbglab: https://github.com/bbglab/qmap
* QMap tool calls two conda environments, stored in conda_env folder.

## Run the pipeline
* From the root directory:
```
$ python run.py
```
