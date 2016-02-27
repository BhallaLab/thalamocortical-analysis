library(ggplot2)
normdata = read.csv('norm_prepost_spikes_DeepBasket_20.0ms_window.csv')
summary(normdata)

##****The pre-stimulus population spike rate goes down with dbcount
qplot(normdata$dbcount, normdata$premean, geom=c("point", "smooth"), method="lm")
# Variability and mean goes down with increasing dbcount
qplot(normdata$dbcount, log(normdata$premean), geom=c("point", "smooth"), method="lm")
# log is not much better
premean.lm <- lm(log(premean) ~ dbcount, data=normdata)
summary(premean.lm)
#Insignificant effet of dbcount
fligner.test(log(premean) ~ dbcount, data = normdata)
## heterogeneity of variance is not significant

ggplot(normdata,aes(x=premean,y=postmean)) +  geom_point() +  stat_smooth(method=lm)
## There is a linear relationship between premean and postmean

# A straightforward linear model shows significance of only premean
prepost.lm = lm(postmean ~ premean * dbcount, data=normdata)
summary(prepost.lm)

basketcells <- normdata$dbcount
qplot(log(normdata$premean), log(normdata$postmean), colour=basketcells,  xlab="pre-stimulus", ylab="post-stimulus", geom=c("point", "smooth"), method="lm")
## This is for dumping fig to file
## png("pre_post_stim_correlation_10ms.png", width=400, height=300)
## myplot = qplot(log(normdata$premean), log(normdata$postmean), colour=basketcells,  xlab="log pre-stimulus", ylab="log post-stimulus", geom=c("point", "smooth"), method="lm")
## par(new=F)
## myplot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())

## dev.off()
cor.test(log(normdata$premean), log(normdata$postmean))
cor.test(normdata$premean, normdata$postmean)


## ##**** Check the relatoin of increment in population spiking due to stimulus
## spike_incr = normdata$postmean - normdata$premean
## qplot(normdata$dbcount, spike_incr,  xlab="# of basket cells", ylab="increase in mean spiking", geom=c("point", "smooth"), method="lm")
## # From the plot it seems that the difference slightly increases with DB count
## #Check the residual plot
## incr.lm <- lm(postmean - premean ~ dbcount, data=normdata)
## summary(incr.lm)
## incr.res <- resid(incr.lm)
## plot(normdata$dbcount, incr.res, xlab="basket cells", ylab="residual", main="Increase in spiking")
## # Looks equally distributed around 0, homoscedastic - for 10 ms window. Not for 20 ms window.
## #****** Wed Jun  3 23:12:20 EDT 2015 given the post-mean is very large compared to pre-mean, increment may be a bad measure.


#**** Check the SEM of the mean population spike rate before stimulus
## sem <- function(x) sqrt(var(x)/length(x))
## dbcounts <- unique(normdata$dbcount)
## for (n in dbcounts){
##     ngrp <- normdata[normdata$dbcount == n,]
##     premean.sem <- sem(ngrp$premean)
##     print(n)
##     print(premean.sem)
## }
## premean.sembydbcount <- aggregate(normdata$premean, by=list(normdata$dbcount), FUN = sem)
## print(premean.sembydbcount)
## plot(premean.sembydbcount)

## # PSTH is a mean by definition - so ignore this
## premedian.sembydbcount <- aggregate(normdata$premedian, by=list(normdata$dbcount), FUN = sem)
## print(premedian.sembydbcount)    

## plot(log(normdata$dbcount), log(normdata$premedian))
## plot(normdata$dbcount, normdata$premean)
## plot(normdata$dbcount, normdata$postmean)
## plot(normdata$dbcount, normdata$prestd)
## plot(log(normdata$dbcount), log(normdata$prestd))
## plot(log(normdata$dbcount), log(normdata$poststd))

## boxplot(log(prestd)~log(dbcount), data=normdata)
## boxplot(postmean~dbcount, data=normdata)
## boxplot(poststd~dbcount, data=normdata)
## fit <- lm(log(prestd)~log(dbcount), data=normdata)
## summary(fit)
## fit <- lm(log(poststd)~log(dbcount), data=normdata)
## summary(fit)
## print("Standard deviation ")
## lognormdata = read.csv('lognorm_prepost_spikes_SpinyStellate_10.0ms_window.csv')
## boxplot(premean~dbcount, data=lognormdata)
## boxplot(prestd~log(dbcount), data=lognormdata)
## boxplot(postmean~dbcount, data=lognormdata)
## boxplot(log(poststd)~dbcount, data=lognormdata)
## print("Standard deviation ")

## boxplot(X0~dbcount, data=data)
