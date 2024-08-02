wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))

library(dplyr)

lilac <- read.csv(paste0(REF_DIR, "lilac_from_fran.csv"), sep = ";",stringsAsFactors = FALSE)
aneuploidy <- read.csv(paste0(REF_DIR, "aneuploidy_scores_from_fran.csv"), sep = ";",stringsAsFactors = FALSE)

k <- i %>% left_join( (j %>% rename(sample_id = "ID_meta_hmfSampleId")), by = "sample_id")

lilac <-
lilac %>% 
  left_join( (aneuploidy %>% rename(sample_id = "ID_meta_hmfSampleId")), by = "sample_id") %>% 
  rename_with( ~ paste0("lilac_", .x)) %>% 
  mutate(ID_meta_hmfSampleId = lilac_sample_id) %>% 
  transmute(ID_meta_hmfSampleId,
            lilac_imbalance = lilac_imbalance_lilac,
            lilac_germline_alleles = lilac_n_germline_alleles, 
            lilac_mut_hla = lilac_mut_HLA,
            lilac_del_hla = lilac_LOH_DEL_HLA,
            lilac_targeted_escape = lilac_targeted_escape..HLA., 
            lilac_non_targeted_escape = lilac_non_targeted_escape..no.HLA., 
            lilac_genetic_immune_escape = lilac_genetic_immune_escape..GIE.,
            lilac_aneuploidy_score)

cols <- sapply(lilac, is.logical)
lilac[,cols] <- lapply(lilac[,cols], as.numeric)
lilac <- (lilac %>% rename_at(vars(-ID_meta_hmfSampleId), function(x){paste0("hla_", x)}))

write.csv(lilac, paste0(TMP_DIR, "lilac_ready.csv"),row.names=FALSE)
