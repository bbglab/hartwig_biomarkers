library(deconstructSigs)

format_for_deconstruct_sigs <- function( cosmic_file ){
    i_file <- read.table(cosmic_file, header = TRUE, stringsAsFactors = FALSE)
    t_file <- t(i_file)
    df <- t_file[-1,]
    colnames(df) <- t_file[1,]
    df <- as.data.frame(df)
    indx <- sapply(df, is.factor)
    df[indx] <- lapply(df[indx], function(x) as.numeric(as.character(x)))
    df
}
get_sigs_wts <- function( sigs_input ){
    sigs_output = whichSignatures(tumor.ref = sigs_input,
                                   signatures.ref = signatures.cosmic.3,
                                   signature.cutoff = 0,
                                   contexts.needed = TRUE)
    sigs_output$weights
}
get_sigs <- function (tncs, i) {
    tnc_sample <- tncs %>% filter(sampleId == i) %>% select(-sampleId)
    rownames(tnc_sample) <- "current_sample"
    sig_wts <- get_sigs_wts(tnc_sample)
    colnames(sig_wts) <- paste("sig", colnames(sig_wts), sep = "_")
    sig_wts <- cbind( "sampleId" = i, sig_wts )
    sig_wts
}
get_sigs_tmb <- function( sigs, sbs_tmb ){
    zipper <- sigs %>% inner_join( sbs_tmb, by = "sampleId")
    tncs <- zipper %>% select(-sampleId, -sbs_tmb)
    tmb <- zipper %>% pull(sbs_tmb)
    sig_tmb <- tncs*tmb
    colnames(sig_tmb) <- unlist(lapply( colnames(sig_tmb), function(i) gsub("sig_", "somatic_TMB_", i)))
    sig_tmb <- cbind( "sampleId" = zipper %>% pull(sampleId), sig_tmb)
    sig_tmb
}
