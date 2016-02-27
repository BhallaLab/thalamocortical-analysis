library(ggplot2)

normdata <- read.table("norm_syncspike_stats_cutoff_0.2_binwidth_5.0ms_lookahead_10.csv", header=TRUE, sep=" ")
#**** Check the SEM of the mean population spike rate before stimulus
sem <- function(x) sqrt(var(x)/length(x))
dbcounts <- unique(normdata$dbcount)
for (n in dbcounts){
    ngrp <- normdata[normdata$dbcount == n,]
    frac_med.sem <- sem(ngrp$frac_med)
    print(n)
    print(frac_med.sem)
}
frac_med.sembydbcount <- aggregate(normdata$frac_med, by=list(normdata$dbcount), FUN = sem)
print(frac_med.sembydbcount)
plot(frac_med.sembydbcount)
##Nothing very striking
dbcounts <- unique(normdata$dbcount)
for (n in dbcounts){
    ngrp <- normdata[normdata$dbcount == n,]
    frac_med.mad <- mad(normdata$frac_med, center = median(ngrp$frac_med), constant = 1,  na.rm = FALSE, low = FALSE, high = FALSE)
    print(n)
    print(frac_med.mad)
}

fracmed.mad <- aggregate(normdata$frac_med, by=list(normdata$dbcount), FUN=mad)
fracmed.mad
