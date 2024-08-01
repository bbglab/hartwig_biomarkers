# 7_get-sigs

## 0_get-sigs
* purpose: extract raw data needed to compute signatures in deconstruct_sigs.
* input: somatic data files
* output: directory full of dataframes formatted for deconstruct_sigs for each sampleId.

## 1_get-sigs
* purpose: compute mutational signatures (no pre-compute)
* input: output from 0_get-sigs
* output: dataframe with each row corresponding to sampleId and columns corresponding to signature exposures.
