wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))
source(paste0(wd,"/mission_control/clinical_help.R"))

library(dplyr)
library(tidyr)

clinical <- read.csv(paste0( TMP_DIR,'clinical_short.csv'), header=TRUE, sep = ",", stringsAsFactors=FALSE)

cpi <- (
    clinical 
        %>% filter(clinical_post_contains_Immunotherapy == "True")
        %>% group_by(patientIdentifier) 
        %>% mutate(ct = n(), sample_order = rank(sampleId)) 
        %>% ungroup()
        %>% arrange(patientIdentifier)
)  
non_dup <- cpi %>% filter( ct == 1) %>% select(-ct, -sample_order)
keep_samples <- c("CPCT02010503TII", "CPCT02020670T", "CPCT02020958TII", "CPCT02050073TII", "CPCT02050276TII", "CPCT02080266T")
dup <- cpi %>% filter(sampleId %in% keep_samples) %>% select(-ct, -sample_order)
cpis <- rbind(non_dup, dup)

non_cpis <- (
    clinical 
        %>% filter(clinical_post_contains_Immunotherapy != "True", 
                   !(patientIdentifier %in% cpi$patientIdentifier))
        %>% group_by(patientIdentifier) 
        %>% mutate(sample_order = rank(desc(sampleId)) )
        %>% ungroup()
        %>% filter(sample_order == 1)
        %>% select(-sample_order))

clinical <- rbind(cpis,non_cpis)

clinical <- clinical %>% select(sampleId, 
                                patientIdentifier,
                                ID_meta_hmfSampleId, 
                                Filter_meta_responseMeasured, 
                                Y_best_response_binary,
                                Y_best_response, 
                                Y_best_response_time_in_days, 
                                Y_relapse, 
                                Survival_pfs_event, 
                                Survival_time_to_pfs_event,
                                Survival_patient_died,
                                Survival_time_to_last_response,
                                Survival_at_6_months,
                                Survival_at_12_months,
                                Survival_at_18_months, 
                                contains("clinical"))
clinical$clinical_tumor_location_group <- unlist(lapply(clinical$clinical_tumor_location_group, tissue))
clinical$clinical_meta_primaryTumorLocation <- unlist(lapply(clinical$clinical_meta_primaryTumorLocation, tissue))
clinical$clinical_meta_consolidatedTreatmentType <- unlist(lapply(clinical$clinical_meta_consolidatedTreatmentType, therapy))
clinical$clinical_meta_hasRadiotherapyPreTreatment <- ifelse(clinical$clinical_meta_hasRadiotherapyPreTreatment == "Yes", 1, 0)
clinical$clinical_meta_hasSystemicPreTreatment <- ifelse(clinical$clinical_meta_hasSystemicPreTreatment == "Yes", 1, 0)
clinical$clinical_meta_gender <- ifelse(clinical$clinical_meta_gender == "female", 1, 0)
clinical$clinical_pre_contains_Chemotherapy <- ifelse(clinical$clinical_pre_contains_Chemotherapy == "True", 1, 0)
clinical$clinical_post_contains_Chemotherapy <- ifelse(clinical$clinical_post_contains_Chemotherapy == "True", 1, 0)
clinical$clinical_pre_contains_Hormonal <- ifelse(clinical$clinical_pre_contains_Hormonal == "True", 1, 0)
clinical$clinical_post_contains_Hormonal <- ifelse(clinical$clinical_post_contains_Hormonal == "True", 1, 0)
clinical$clinical_pre_contains_Immunotherapy <- ifelse(clinical$clinical_pre_contains_Immunotherapy == "True", 1, 0)
clinical$clinical_pre_contains_Targeted <- ifelse(clinical$clinical_pre_contains_Targeted == "True", 1, 0)
clinical$clinical_post_contains_Targeted <- ifelse(clinical$clinical_post_contains_Targeted == "True", 1, 0)
clinical$clinical_pre_treated <- as.numeric(clinical$clinical_meta_hasRadiotherapyPreTreatment + clinical$clinical_meta_hasSystemicPreTreatment > 0)
clinical$clinical_prior_therapies <- ( apply(
    clinical %>% select(contains("pre_contains"), clinical_meta_hasRadiotherapyPreTreatment, clinical_pre_treated),
        1, group_prior_therapy))

write.csv( clinical, paste0( TMP_DIR, 'clinical_ready.csv'), row.names = FALSE)
