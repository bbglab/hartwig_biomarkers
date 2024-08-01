# hartwig_biomarkers

## Goal of Repository
* Clean and organize the Hartwig data request files into a single dataframe. 

(overview.pdf)

## Organization
* For each molecular file type, a pipeline computes features across all samples. 
* Output from each pipeline are then joined by their sample ids.
* Helper files to compute features for each molecular file type (*helper*) are located in mission_control folder.  

## Prerequisites to Run

### Approvals
* Need approval to use Hartwig data:
*- See: https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/ 
* Need the Harwig database PURPLE, ISOFOX, and clinical data output. 

### Source and reference data 
* Run and tested on Hartwig data request files shared on August 9, 2022.
* Source file locations need to be specified in mission_control/treasure_map(.py,.R).

### QMap and conda environments
* Jobs are submitted with the QMap tool from the bbglab: https://github.com/bbglab/qmap
* QMap tool calls two conda environments, stored in conda_env folder.

## Run the pipeline
* From the root directory:
```
$ python run.py

```
