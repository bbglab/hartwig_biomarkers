# Overview

## 0_get-clinical

### Purpose
* Organize Hartwig clinical data into a single flat (non-longitudinal) data frame.  

### Input 
* From hartwig directory: metadata.tsv, treatment_responses.tsv, pre_biopsy_drugs.tsv, post_biopsy_drugs.tsv

### Output
* A single file named clinical_short.csv with derived clinical features. 


## 1_get-clinical

### Purpose
* Remove duplicates and add more curated features.

### Input 
* Output from 0_get-clincal: clinical_short.csv

### Output
* A file with only one sample per patient and added features: clinical_ready.csv
