CoreAlg <- function(X, y){

  svn_itor <- 3
  res <- function(i){
    if(i==1){nus <- 0.5}
    if(i==2){nus <- 0.25}
    if(i==3){nus <- 0.75}
    model<-svm(X,y,type="nu-regression",kernel="radial",nu=nus,scale=F)
    model
  }
  out <- mclapply(1:svn_itor, res, mc.cores=svn_itor)
  nusvm <- rep(0,svn_itor)
  corrv <- rep(0,svn_itor)
  
  #do cibersort
  t <- 1
  while(t <= svn_itor) {
    weights = t(out[[t]]$coefs) %*% out[[t]]$SV
    weights[which(weights<0)]<-0
    w<-weights/max(sum(weights),.0001) ### added here
    u <- sweep(X,MARGIN=2,w,'*')
    k <- apply(u, 1, sum)
    nusvm[t] <- sqrt((mean((k - y)^2)))
    corrv[t] <- cor(k, y)
    t <- t + 1
  }
  
  #pick best model
  rmses <- nusvm
  mn <- which.min(rmses) 
  #print(mn)
  model <- out[[mn]]
  mix_rmse <- rmses[mn]
  mix_r <- corrv[mn]
  
  #get and normalize coefficients
  q <- t(model$coefs) %*% model$SV; #w <- q
  q[which(q<0)]<-0
  w <- q/sum(q)
  newList <- list("w" = w, "mix_rmse" = mix_rmse, "mix_r" = mix_r)
}

CIBERSORT <- function(X, Y, QN = FALSE, scale_X = TRUE, scale_Y = FALSE){
  #quantile normalization of mixture file
  # library(preprocessCore)
  if(QN == TRUE){
    tmpc <- colnames(Y)
    tmpr <- rownames(Y)
    Y <- normalize.quantiles(Y)
    colnames(Y) <- tmpc
    rownames(Y) <- tmpr
  }
  if (scale_X == TRUE) X <- scale(X)
  if (scale_Y == TRUE) Y <- scale(Y)
  #iterate through mixtures
  weights <- data.frame()
  stats <- data.frame()
  itor <- 1
  while(itor <= ncol(Y)){
    results <- CoreAlg(X, Y[,itor])
    weights <- rbind(weights, results$w)
    stats <- rbind(stats, data.frame( mix_r = results$mix_r, mix_rmse = results$mix_rmse ))
    itor <- itor + 1
  }
  weights$sampleId <- colnames(Y)
  stats$sampleId <- colnames(Y)
    
  list("wts" = weights, "stats" = stats)
}
