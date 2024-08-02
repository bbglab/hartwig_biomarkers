wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))
source(paste0(wd,"/mission_control/isofox_help.R"))

library(dplyr)
library(tidyverse)
library(data.table)

args <- list("AdjTPM")

REF_DIR

cpi1000_sets <- readRDS(paste0(REF_DIR,"cpi1000_gene_sets.Rds"))
mariathan_sets <- readRDS(paste0(REF_DIR,"human_gene_signatures.Rds"))
tgfb_sets <- readRDS(paste0(REF_DIR,"battle_gene_sets.Rds"))
vhio_sets <- readRDS(paste0(REF_DIR,"vhio_gene_sets.Rds"))
cluster_sets <- readRDS(paste0(REF_DIR,"fig_2and3_clusters.Rds"))

gsea_sets <- readRDS(paste0(REF_DIR,"GSEA_gene_sets.Rds"))
kegg_sets <- gsea_sets[which(unlist(lapply( names(gsea_sets), function(i) grepl("KEGG",i))))]
hallmark_sets <- gsea_sets[which(unlist(lapply( names(gsea_sets), function(i) grepl("HALLMARK",i))))]
go_sets <- gsea_sets[which(unlist(lapply( names(gsea_sets), function(i) grepl("_GO_",i))))]                                               

isofox <- fread(paste0( TMP_DIR,"isofox_",args[1],"_features.csv"))

isofox2 <- isofox %>% mutate_at(vars(-sampleId), ~(log(.+1) %>% as.vector))

names(mariathan_sets) <- gsub(" ", "_", names(mariathan_sets))
names(mariathan_sets) <- unlist(lapply(names(mariathan_sets), function(i) paste0("gene_set_mariathan_", i)))

names(cluster_sets) <- unlist(lapply(names(cluster_sets), function(i) paste0("gene_set_", i)))
names(tgfb_sets) <- unlist(lapply(names(tgfb_sets), function(i) paste0("gene_set_", i)))
names(vhio_sets) <- unlist(lapply(names(vhio_sets), function(i) paste0("gene_set_", i)))
names(kegg_sets) <- unlist(lapply(names(kegg_sets), function(i) paste0("gene_set_", i)))
names(hallmark_sets) <- unlist(lapply(names(hallmark_sets), function(i) paste0("gene_set_", i))) 
names(go_sets) <- unlist(lapply(names(go_sets), function(i) paste0("gene_set_", i)))                                                                             

gene_sets <- c(cpi1000_sets, mariathan_sets, tgfb_sets, vhio_sets, kegg_sets, hallmark_sets, go_sets, cluster_sets)

names(gene_sets) <- paste0("isofox_", names(gene_sets))

appender <- function(ll) unlist(lapply( ll, function(i) gsub("-",".",paste0("isofox_", i))))
for (i in names(gene_sets)) gene_sets[[i]] <- appender(gene_sets[[i]])

gene_sets[['isofox_gene_set_mariathan_Histones']] <- NULL
gene_sets[['isofox_CD_8_T_EFFECTOR']] <- NULL

gene_sets_ls <- list()
for (i in names(gene_sets)){
    print(i)
    flush.console()
    tmp <- isofox2 %>% select(any_of(gene_sets[[i]]))
    gene_sets_ls[[i]] <- apply(tmp, 1, mean, na.rm = TRUE)
}
gene_sets_final <- data.frame(gene_sets_ls)
gene_sets_final$sampleId <- isofox2 %>% pull(sampleId)

happy_isofox <- isofox2 %>% left_join(gene_sets_final, by = "sampleId")
rownames(happy_isofox) <- NULL

fwrite( happy_isofox, file = paste0( TMP_DIR, "isofox_", args[1], "_ready.csv") )
