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

clinical$clinical_number_pretreatment <- unlist(lapply(clinical$ID_pre_name, function(i) length(strsplit(i, "/")[[1]])))

trt_mechanisms <- unique(unlist(lapply(clinical$ID_post_mechanism, function(i) strsplit(i, "/")[[1]])))
                                       
sizes <- data.frame()
for (i in c(trt_mechanisms, "Pyrimidine", "GnRH")){
    size <- data.frame( "trt_mechanism" = i, ct = nrow(clinical %>% filter(grepl(i, ID_post_mechanism))))
    sizes <- rbind(sizes, size) 
}
sizes <- sizes %>% arrange(desc(ct)) %>% filter(trt_mechanism != "inhibitor") %>% filter(ct > 20)
                                       
for( i in sizes$trt_mechanism ){
    clean_mech <- gsub("[^[:alnum:] ]","",i)
    field_name <- paste0("clinical_trt_mechanism_contains_", clean_mech )
    clinical[,field_name] <- ifelse( grepl(i, clinical$ID_post_mechanism), 1, 0)
}                                        

subtypes <- (
    clinical 
        %>% filter(clinical_meta_primaryTumorLocation %in% c("Breast", "Lung")) 
        %>% group_by(ID_meta_primaryTumorSubType) 
        %>% summarise(ct = n()) 
        %>% arrange(desc(ct)) 
        %>% filter(ct > 20)
        %>% pull(ID_meta_primaryTumorSubType)
)

for( i in subtypes ){
    clean_subtype <- gsub(" ", "_", gsub("[^[:alnum:] ]","_",i))
    print(clean_subtype)
    field_name <- paste0("clinical_subtype_", clean_subtype )
    clinical[,field_name] <- ifelse( grepl(i, clinical$ID_meta_primaryTumorSubType), 1, 0)
}        

#clinical %>% filter(clinical_trt_mechanism_contains_Platinum == 1) %>% group_by( clinical_meta_primaryTumorLocation ) %>% summarise(ct = n()) %>% arrange(desc(ct))

clinical$clinical_tumor_location_group <- unlist(lapply(clinical$clinical_tumor_location_group, tissue))
clinical$clinical_meta_primaryTumorLocation <- unlist(lapply(clinical$clinical_meta_primaryTumorLocation, tissue))
clinical$clinical_meta_consolidatedTreatmentType <- unlist(lapply(clinical$clinical_meta_consolidatedTreatmentType, therapy))
clinical$clinical_meta_hasRadiotherapyPreTreatment <- ifelse(clinical$clinical_meta_hasRadiotherapyPreTreatment == "Yes", 1, 0)
clinical$clinical_meta_hasSystemicPreTreatment2 <- ifelse(clinical$clinical_meta_hasSystemicPreTreatment == "Yes", 1, 0)
clinical$clinical_meta_gender <- ifelse(clinical$clinical_meta_gender == "female", 1, 0)
clinical$clinical_pre_contains_Chemotherapy <- ifelse(clinical$clinical_pre_contains_Chemotherapy == "True", 1, 0)
clinical$clinical_post_contains_Chemotherapy <- ifelse(clinical$clinical_post_contains_Chemotherapy == "True", 1, 0)
clinical$clinical_pre_contains_Hormonal <- ifelse(clinical$clinical_pre_contains_Hormonal == "True", 1, 0)
clinical$clinical_post_contains_Hormonal <- ifelse(clinical$clinical_post_contains_Hormonal == "True", 1, 0)
clinical$clinical_pre_contains_Immunotherapy <- ifelse(clinical$clinical_pre_contains_Immunotherapy == "True", 1, 0)
clinical$clinical_pre_contains_Targeted <- ifelse(clinical$clinical_pre_contains_Targeted == "True", 1, 0)
clinical$clinical_post_contains_Targeted <- ifelse(clinical$clinical_post_contains_Targeted == "True", 1, 0)
clinical$clinical_pre_treated <- as.numeric(clinical$clinical_meta_hasRadiotherapyPreTreatment + clinical$clinical_meta_hasSystemicPreTreatment2 > 0)
clinical$clinical_cpi_mechanism <- get_cpi_mechanism(clinical$clinical_meta_treatment)
clinical$clinical_cpi_mechanism2 <- ifelse( clinical$clinical_cpi_mechanism %in% c("PD1", "PDL1"), "PD", clinical$clinical_cpi_mechanism)
clinical$clinical_cpi_mechanism3 <- ifelse( clinical$clinical_cpi_mechanism == "multiple", 1, 0)
clinical$clinical_systemic_composite <- (
        ifelse(clinical$clinical_meta_hasSystemicPreTreatment2 == 0, 
               365*10, 
               clinical$clinical_pre_to_post_treatment_time
              )
)
clinical$clinical_multiple_treatment = ifelse( clinical$clinical_meta_consolidatedTreatmentType == "multiple", 1,0) 

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
                                Survival_os_event,
                                Survival_time_to_os_event,
                                Survival_at_6_months,
                                Survival_at_12_months,
                                Survival_at_18_months, 
                                contains("clinical"))

write.csv( clinical, paste0( TMP_DIR, 'clinical_ready.csv'), row.names = FALSE)
