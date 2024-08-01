group_prior_therapy <- function( i ){
    if( i[6] == 0){
        "Unknown"
    } else if ( (i[1] + i[2] + i[3] + i[4] + i[5]) > 1 ){
        "Multiple"
    } else if ( i[1] == 1 ){
        "Chemotherapy"
    } else if ( i[5] == 1){
        "Radiotherapy"
    } else {
        "Other"
    }
}
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
cpi_drugs <- list(
    "Pembrolizumab" = "PD1",
    "Nivolumab" = "PD1",
    "Avelumab" = "PDL1",
    "PD-L1 antibody" = "PDL1",
    "Atezolizumab" = "PDL1",
    "Durvalumab" = "PDL1",
    "Ipilimumab" = "CTLA4",
    "Tremelimumab" = "CTLA4"
)
get_mechs <- function( l ){
    i <- l[[1]]
    if( sum(i) > 1){
        "multiple"
    } else if ( i['PD1']){
        'PD1'
    } else if ( i['CTLA4']){
        'CTLA4'
    } else if ( i['PDL1']){
        'PDL1'
    } else {
        'Non_CPI'
    } 
}
get_cpi_mechanism <- function( treatment_lists ){
    drug_list <- list()
    for (i in names(cpi_drugs)) {
        drug_list[[i]] <- unname(
            sapply(treatment_lists,function(l) as.numeric(grepl(i,l)))
        ) 
    }
    mech_list <- list( 
        'PD1'   = drug_list[['Pembrolizumab']] + drug_list[['Nivolumab']],
        'CTLA4' = drug_list[['Ipilimumab']] + drug_list[['Tremelimumab']],
        'PDL1'  = (drug_list[['Avelumab']] + drug_list[['PD-L1 antibody']] 
                 + drug_list[['Atezolizumab']] + drug_list[['Durvalumab']])
    )
    patient_mechs <- apply(data.frame(mech_list),1,list)                                 
    cpi_mechanisms <- unlist(lapply( patient_mechs, get_mechs ) )    
    cpi_mechanisms
}

