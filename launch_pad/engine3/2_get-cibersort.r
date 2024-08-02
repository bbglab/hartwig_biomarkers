wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))
source(paste0(wd,"/mission_control/cibersort_help.R"))

library(e1071)
library(parallel)
library(dplyr)

args <- commandArgs(trailing = TRUE) ## "RawTPM" or "AdjTPM" #
#args <- list("AdjTPM", "LM22")

mixture <- read.csv(paste0(TMP_DIR, "cibersort_prep_", args[1], ".csv"))

sig_ref <- read.csv(paste0(REF_DIR, args[2], ".txt"), sep = "\t")
tag <- strsplit(unlist(args[2]), ".txt")[[1]][1]

if( tag == "TR4"){
  sig_ref <- 
    sig_ref %>% 
      rename( Gene.symbol = NAME,  epithelial = EPCAM, fibroblasts = CD10, endothelial = CD31, immune = CD45)
}

mixture_ready <- mixture[which(mixture$GeneName %in% sig_ref$Gene.symbol),]
sig_ref_ready <- sig_ref[which(sig_ref$Gene.symbol %in% mixture$GeneName),]
X <- data.matrix(sig_ref_ready[,-1])
Y <- data.matrix(mixture_ready[,-1])

out <- CIBERSORT( X, Y )

cibersort_features <- 
    (out$wts 
        %>% left_join(out$stats, by = "sampleId") 
        %>% rename_at(vars(-sampleId), ~ paste0("cibersort_", tag, "_", .x))
        %>% relocate(sampleId))
write.csv( cibersort_features, file = paste0(TMP_DIR, "cibersort_", args[1],"_", args[2], "_ready.csv"), row.names=FALSE)
