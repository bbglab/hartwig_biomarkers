# 3_get-isofox

## isofox
* Purpose: Extract log-transformed gene expression across encode genes, and also mean gene-set expressions. 
* Input: Isofox input files from hartwig (collected from 1_create-file-index).
* Output: Large dataframe with sampleIds on each row and expression features for each column.  

## neoepitopes
* Purpose: Extract predicted neoepitopes for each patient. 
* Input: Neoepitope input files (collected from 1_create-file-index)
* Output: Dataframe with sampleIds on each row and a predicted neoepitope column.

## cibersort
* Purpose: Compute cell-type prevalence using cibersort tool.  
* Input: Output from 1_get-isofox/isofox pipeline.
* Output: Dataframe with sampleIds on each row and estimated cell-type prevalence in columns.
