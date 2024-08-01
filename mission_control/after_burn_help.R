library(tidyr)
library(dplyr)

tissue <- function(i){
    i <- tolower(i)
    i <- gsub(" ", "_",i)
    i <- gsub("/", "_",i)
    if (i == "urothelial_tract"){
        "bladder"
    } else {
        i
    }
}
therapy <- function(i){
    start <- tolower(strsplit(i," ")[[1]][1])
    if( grepl(start, "androgen")){
        'hormonal'
    } else if (start %in% c('hormonal','multiple','targeted','immunotherapy','chemotherapy')){
        start
    } else {
        'other'
    }
}
give_me_pcs <- function( df, match, scale = FALSE ){
    hold <- (
        df 
            %>% select("sampleId",contains(match)) 
            %>% select_if(~sum(!is.na(.)) > 0)
            %>% drop_na()
            %>% mutate_at(vars(-sampleId), ~scale(.x))
            %>% select_if(~sum(!is.na(.)) > 0)
    )
    twirl <- prcomp(as.matrix(hold[,-1]))
    keep <- min( min(which(cumsum(twirl$sdev^2)/sum(twirl$sdev^2) > .95)),20)
    meld <- data.frame(cbind("sampleId" = hold$sampleId, twirl$x[,1:keep]))
    idx <- seq(ncol(meld))[-1]
    meld[idx] <- lapply(meld[idx], function(x) as.numeric(as.character(x)))
    meld %>% rename_at(vars(-sampleId), ~ paste0(paste0(substr(match,1,nchar(match)-1),".pc_"),.x))
}
