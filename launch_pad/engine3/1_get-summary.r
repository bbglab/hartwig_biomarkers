wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))

library(dplyr)
library(tidyr)

summary <- read.csv( paste0( TMP_DIR, "summary_features.csv"), stringsAsFactors = FALSE)

summary <- (
        summary %>% select(
                sampleId,
                summary_diploidProportion,
                summary_ploidy,
                summary_polyclonalProportion,
                summary_wholeGenomeDuplication,
                summary_purity,
                summary_msIndelsPerMb,
                summary_msStatus,
                summary_tml,
                summary_tmlStatus,
                summary_tmbPerMb,
                summary_tmbStatus,
                summary_svTumorMutationalBurden
                ))

summary$summary_wholeGenomeDuplication <- ifelse(summary$summary_wholeGenomeDuplication== "True", 1, 0)
summary$summary_msStatus <- ifelse(summary$summary_msStatus== "MSI", 1, 0)
summary$summary_tmlStatus <- ifelse(summary$summary_tmlStatus== "HIGH", 1, 0)
summary$summary_tmbStatus <- ifelse(summary$summary_tmbStatus== "HIGH", 1, 0)

summary <- (summary %>% mutate_at(
                            vars( summary_msIndelsPerMb,
                                  summary_tml,
                                  summary_tmbPerMb,
                                  summary_svTumorMutationalBurden), 
            ~((log(.+1) %>% as.vector))))

summary <- (summary %>% rename_at(vars( summary_svTumorMutationalBurden ), function(x){paste0("sv_", x)}))
summary <- (summary %>% rename_at(vars( summary_diploidProportion,
                                        summary_ploidy,
                                        summary_polyclonalProportion,
                                        summary_wholeGenomeDuplication),
                         function(x){paste0("cnv_", x)}))

summary <- (summary %>% rename_at(vars( summary_purity,
                                        summary_msIndelsPerMb,
                                        summary_msStatus,
                                        summary_tml,
                                        summary_tmlStatus,
                                        summary_tmbPerMb,
                                        summary_tmbStatus),
                         function(x){paste0("somatic_", x)}))

write.csv( summary, paste0( TMP_DIR, 'summary_ready.csv'), row.names = FALSE)
