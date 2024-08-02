wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))
source(paste0(wd,"/mission_control/sigs_help.R"))

library(deconstructSigs)
library(dplyr)

signatures.cosmic.3 <- format_for_deconstruct_sigs(paste0( REF_DIR,'COSMIC_v3.2_SBS_GRCh37.txt') )

tncs <- read.csv( paste0( SIGS_DIR,"tncs.csv"),check.names=FALSE, stringsAsFactors = FALSE) %>% select(-"")
tmb <- data.frame( "sampleId" = tncs$sampleId, "sbs_tmb" = apply( tncs %>% select(-sampleId),1,sum))

sigs <- data.frame(); j <- 0
system.time(
for (i in (tncs %>% pull(sampleId))){
    print(paste0( j )); j <- j+1
    flush.console()
    sigs_i <- get_sigs(tncs, i)
    sigs <- rbind(sigs, sigs_i)
}
)

sigs_tmb <- get_sigs_tmb( sigs, tmb )
sig_tmb_join <- inner_join(sigs, sigs_tmb, by = "sampleId")
sigs_output <- sig_tmb_join %>% mutate_at(vars(-contains("sig_"), -sampleId), ~(log(.+1) %>% as.vector))

write.csv( sigs_output, paste0( TMP_DIR,'sigs_ready.csv'), row.names = FALSE)
