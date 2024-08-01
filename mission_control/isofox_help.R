gene_sets = list(
    'gene_set_cyt' = c('GZMA', 'PRF1'),
    'gene_set_t_cell_gep_6' = c('IFNG','STAT1','CXCL9','CXCL10','IDO1', 'HLA-DRA'),
    'gene_set_t_cell_gep_10' = c('GZMA', 'PRF1', 'IFNG','STAT1','CCR5','CXCL9','CXCL10','CXCL11','IDO1','HLA-DRA'),
    'gene_set_t_cell_gep_18' =  c('CD3D','IDO1','CIITA','CD3E','CCL5','GZMK','CD2','HLA-DRA','CXCL13','IL2RG','NKG7','HLA-E','CXCR6','LAG3','TAGAP','CXCL10','STAT1','GZMA','GZMB'),
    'gene_set_prolif' = c('BUB1','CCNB2','CDK1','CDKN3','FOXM1','KIAA0101','MAD2L1','MELK','MKI67','TOP2A'),
    'gene_set_tim3' = c('HAVCR2', 'LAG3', 'PDCD1', 'CTLA4', 'C10orf54', 'BTLA', 'FOXP3'),
    'gene_set_t_cell_effector' = c('CD8A','CD27','IFNG','GZMA','GZMB','PRF1','EOMES','CXCL9','CXCL10','CXCL11','CD274','CTLA4','FOXP3','TIGIT','IDO1','PSMB8','PSMB9','TAP1','TAP2'),
    'gene_set_myeloid_inflammation' = c('CXCL1','CXCL2','CXCL3','IL8','IL6','PTGS2'),
    'gene_set_stroma_emt_shortened' = c('FLNA','EMP3','CALD1','FN1','FOXC2','LOX','FBN1','TNC'),
    'gene_set_Pan_TBRS' = c('TGFB1','TGFBR2','ACTA2','COL4A1','TAGLN','SH3PXD2A'),
    'gene_set_impres' = c('PDCD1','CD27','CTLA4','CD40','CD86','CD28','CD80','TNFRSF14','TNFSF4','TNFRSF9','C10orf54','HAVCR2','CD200','CD276','CD274'), ### based on pairwise comparisons
    'gene_set_12_chemokine' = c('CCL2', 'CCL3', 'CCL4','CCL5','CCL8','CCL18','CCL19','CCL21','CXCL9','CXCL10','CXCL11','CXCL13'), ### usa PCA to combine (1st PC)
    'gene_set_immune_checkpoint_genes' = c('CD8A','PDCD1','CD274','PDCD1LG2','CTLA4','CD80','CD86','BTLA','TNFRSF14','LAG3'), ### from herv-3 paper
    'gene_set_cd8_t_effector' = c('CD8A','GZMA','GZMB','IFNG', 'CXCL9','CXCL10','PRF1','TBX21'),
    'gene_set_infiltrate'  = c('CD247', 'CD2', 'CD3E', 'GZMH', 'NKG7', 'PRF1','GZMK'),
    'gene_set_t_cell_rand1' = c('IL21R','SLAMF7','FASLG','CXCR6','HLA-E','NCKAP1L','CST7','CD96'),
    'gene_set_prolif_rand1' = c('CHEK1', 'ERCC6L', 'CKAP2', 'KIF14', 'NCAPG2','SKA1','KIF15','PRC1'),
    'gene_set_tgfb_rand1' = c('BGN','COL5A1','PCDH12','COL1A2','JCAD','COL1A1','ESAM','CDH5')
)
surgeon <- function(i){
    if (grepl("gene_set_m_", i)){
        strsplit(i,"gene_set_m_")[[1]][2]
    } else {
        strsplit(i,"gene_set_")[[1]][2]
    }
}

