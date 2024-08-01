wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))
source(paste0(wd,"/mission_control/after_burn_help.R"))

library(tidyverse)
library(data.table)

args <- list("AdjTPM")

setwd(TMP_DIR)

clinical       <- fread( "clinical_ready.csv" )
summary        <- fread( "summary_ready.csv" )
sigs           <- fread( "sigs_ready.csv" )
cibersort_lm22 <- fread( paste0("cibersort_", args[1],"_LM22_ready.csv") )
cibersort_tr4  <- fread( paste0("cibersort_", args[1],"_TR4_ready.csv") )
drivers        <- fread( "driver_ready.csv" )
hlas           <- fread( "hla_ready.csv" )
isofox         <- fread( paste0("isofox_", args[1], "_ready.csv") )
somatic        <- fread( "somatic_ready.csv" )
cnv            <- fread( "cnv_ready.csv" )
cnv_gene       <- fread( "cnv_gene_ready.csv" )
neoepitope     <- fread( "neoepitope_ready.csv" )
sv             <- fread( "sv_ready.csv" )
lilac          <- fread( "lilac_ready.csv")

somatic <- somatic %>% mutate(somatic_clonal_pct = somatic_TMB_clonal/somatic_TMB)
somatic$somatic_TMB_exome <- apply( somatic %>% select(contains(".gene")), 1, sum)

somatic <- somatic %>% mutate_at(vars(-sampleId, -somatic_clonal_pct), ~(log(.+1) %>% as.vector))
cnv <- cnv %>% mutate_at( vars(-sampleId), ~(log(.+1) %>% as.vector))
cnv_gene <- cnv_gene %>% mutate_at(vars(-contains("_loh_"), -sampleId), ~(log(.+1) %>% as.vector))
neoepitope <- neoepitope %>% mutate_at(vars(-sampleId), ~(log(.+1) %>% as.vector))
sv <- sv %>% mutate_at(vars(-sampleId), ~(log(.+1) %>% as.vector))

all <- (
    clinical
        %>% left_join(hlas, by='sampleId')
        %>% left_join(cibersort_lm22, by='sampleId')
        %>% left_join(cibersort_tr4, by='sampleId')
        %>% left_join(cnv, by='sampleId')
        %>% left_join(cnv_gene, by='sampleId')
        %>% left_join(drivers, by='sampleId')
        %>% left_join(isofox, by='sampleId')
        %>% left_join(neoepitope, by='sampleId')
        %>% left_join(sigs, by='sampleId')
        %>% left_join(somatic, by='sampleId')
        %>% left_join(summary, by='sampleId') 
        %>% left_join(sv, by='sampleId')   
        %>% left_join(lilac, by='ID_meta_hmfSampleId')
    )

#all %>% select(contains("cluster"))

#all <- 
#    (all 
#         %>% left_join( give_me_pcs(somatic, "somatic_"), by = "sampleId")
#         %>% left_join( give_me_pcs(somatic, "somatic.gene_"), by = "sampleId")
#         %>% left_join( give_me_pcs(isofox, "isofox"), by = "sampleId")
#         #%>% left_join( give_me_pcs(cnv_gene, "cnv.region_cn_"), by = "sampleId")
#)

fwrite( all, file=paste0( CLN_DIR, "signals_base.csv") )
