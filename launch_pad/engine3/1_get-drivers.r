wd <- dirname(getwd())
source(paste0(wd,"/mission_control/treasure_map.R"))

library(tidyr)
library(dplyr)

drivers_purple <- read.csv( paste0( TMP_DIR,"drivers_DB_purple.csv"), stringsAsFactors = FALSE)
drivers <- (drivers_purple 
                %>% filter(driverLikelihood > .999) 
                %>% transmute( sampleId, driver = paste0(gene,"_",driver))
                %>% distinct())

common_drivers <- (
    drivers
        %>% group_by(driver) 
        %>% summarise(ct = n()) 
        %>% arrange(desc(ct)) 
        %>% filter(ct > 20)
        %>% pull(driver)
)
sampleIds <- unique(drivers %>% pull(sampleId))

genes <- list()
genes[["sampleId"]] <- sampleIds
for (gene in common_drivers){
    cts <- c()
    for (sample in sampleIds){
        cts <- c(cts, nrow(drivers %>% filter(sampleId == sample, driver == gene)))
    }
    genes[[paste0("driver_",gene)]] <- cts
}

write.csv( data.frame(genes), file = paste0( TMP_DIR, "driver_ready.csv"), row.names=FALSE)
