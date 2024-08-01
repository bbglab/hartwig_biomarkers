# 0_get-clinical

## 0_get-clinical

#### Purpose
* Read and curate hartwig clinical data into a single flat (non-longitudinal) data frame.  

#### Input 
* From hartwig directory: metadata.tsv, treatment_responses.tsv, pre_biopsy_drugs.tsv, post_biopsy_drugs.tsv

#### Output
* A single file named clinical_short.csv with derived clinical features. 


## 1_clinical-de-duplicate
#### Purpose
* Remove patient sample duplicates from clinical data

#### Input 
* clinical_short.csv output from 0_get-clinical

### Output
* A file with only one sample per patient: clinical_short_de_duplicate.csv

