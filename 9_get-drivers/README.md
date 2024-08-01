# 9_get-drivers

## 0_get-drivers
* purpose: extract large dataframe of driver data across hartwig patients
* input: list of individual driver files
* output: dataframe of driver information across hartwig patients (both linx and driver)

## 1_get-drivers
* purpose: flatten output from 0_get-drivers, with one row for each sampleId
* input: output from 0_get-drivers
* output: dataframe with each row corresponding to sampleId and feature columns that indicate common drivers.
