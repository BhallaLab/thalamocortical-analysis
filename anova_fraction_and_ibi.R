library(ggplot2)

####################
## Load the data
####################
normdata <- read.table("norm_syncspike_stats_cutoff_0.2_binwidth_5.0ms_lookahead_10.csv", header=TRUE, sep=",")
lognormdata <- read.table("lognorm_syncspike_stats_cutoff_0.2_binwidth_5.0ms_lookahead_10.csv", header=TRUE, sep=",")
## Add a column for distribution of synaptic strengths
normdata["distribution"] <- "normal"
lognormdata["distribution"] <- "lognormal"
## Combined the two datasets into one, where the "distribution" column
## separates the two datasets.
combined = rbind(normdata, lognormdata)
## Make the distribution column into a categorical variable
combined$distribution = factor(combined$distribution)

##################################################################
##################################################################
## Process data for normal distribution of synaptic
## conductances. Analyze synchronously spiking fraction of cells.
##################################################################
##################################################################

## Display some statistics for normal distribution data
head(normdata)
std <- aggregate(frac_median ~ dbcount, normdata, sd)
print("Standard deviation in normal distr data")
print(std)

## Levene's test for homogeneity of variance
## library(car)
## leveneTest(frac_median ~ dbcount, data=normdata)
## Levene's test is not appropriate with quantitative explanatory variables.

## Test for homoscedasticity
fligner.test(frac_median ~ dbcount, data = normdata)
## d20 <- normdata[normdata$dbcount==30,]
## sd(d20[,c('frac_median')])
std <- aggregate(frac_median ~ dbcount, lognormdata, sd)
print("Standard deviation in lognormal distr data")
print(std)
## Test for homoscedasticity
fligner.test(frac_median ~ dbcount, data = lognormdata)
## Welch' test for one way ANOVA
oneway.test(frac_median ~ dbcount, data = normdata)
kruskal.test(frac_median ~ dbcount, data = normdata)
oneway.test(frac_iqr ~ dbcount, data = normdata)

#########################################
## LM: linear regression
#########################################
## Linear regression fit stats
lmfit = lm(frac_median ~ dbcount, data = normdata)
summary(lmfit)
anova(lmfit, test = "Chisq")
plot(lmfit)

## Plot the fit
png("ss_med_frac_norm_lm_fit.png", width=400, height=300)
lm_plot <- ggplot(normdata, aes(x=dbcount, y=frac_median)) + xlab("basket cells") + ylab("Median fraction") + geom_point(shape=19) + geom_smooth(method="lm")
par(new=F)
lm_plot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())
dev.off()

## This was a trial for log transform
## lmfit = lm(log(frac_median) ~ dbcount, data = normdata)
## summary(lmfit)
## anova(lmfit, test = "Chisq")
## plot(lmfit)

#########################################
## GLM: Binomial fit with logit link
#########################################

## library(MASS)
## boxcox(frac_median ~ dbcount, data=normdata, lambda=seq(-2, 4, by=0.1))
## lmfit = lm(frac_iqr ~ dbcount, data = normdata)
## summary(lmfit)
## #Generalized linear model fit with distribution from Gamma family
## glmfit = glm(frac_median ~ dbcount, family=Gamma, data = normdata)
## summary(glmfit)
## anova(glmfit, test = "Chisq")
## plot(glmfit)

## Binomial is best fit, this is natural when there are two
## possibilities - spiking or nonspiking - logistic model
### Plot the data with fitted model - checked with statsmodels - but
### could not produce the confidence interval
png("ss_med_frac_norm_binomial_fit.png", width=400, height=300)
binom_plot <- ggplot(normdata, aes(x=dbcount, y=frac_median)) + xlab("basket cells") + ylab("Median fraction") + geom_point(shape=19) + geom_smooth(method="glm", family=binomial(logit))
par(new=F)
binom_plot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())
dev.off()

## A more direct of logistic regression and its summary
spiking <- round(normdata$frac_median*240)
nonspiking <- 240 - spiking
dbcount <- normdata$dbcount
ss.logistic = glm(cbind(spiking, nonspiking )~ dbcount, data=normdata, family=binomial)
summary(ss.logistic)

####################################################################
####################################################################
## Process data for lognormal distribution of synaptic
## conductances. Analyze synchronously spiking cell fraction.
####################################################################
####################################################################

##############################################
## Plot linear fit for lognorm distribution
##############################################

png("ss_med_frac_lognorm_lm_fit.png", width=400, height=300)
lm_plot <- ggplot(lognormdata, aes(x=dbcount, y=frac_median)) + xlab("basket cells") + ylab("Median fraction") + geom_point(shape=19) + geom_smooth(method="lm")
par(new=F)
lm_plot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())
dev.off()

##############################################
## Plot binomial fit for lognorm distribution
##############################################
png("ss_med_frac_lognorm_binomial_fit.png", width=400, height=300)
binom_plot <- ggplot(lognormdata, aes(x=dbcount, y=frac_median)) + xlab("basket cells") + ylab("Median fraction") + geom_point(shape=19) + geom_smooth(method="glm", family="binomial")
par(new=F)
binom_plot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())
dev.off()


pairwise.t.test(normdata$frac_median, normdata$dbcount, p.adj="b")
oneway.test(frac_median ~ dbcount, data = lognormdata)
kruskal.test(frac_median ~ dbcount, data = lognormdata)
lmfit = lm(frac_median ~ dbcount, data = lognormdata)
summary(lmfit)
anova(lmfit, test = "Chisq")
lmfit = lm(frac_iqr ~ dbcount, data = lognormdata)
summary(lmfit)
pairwise.t.test(lognormdata$frac_median, lognormdata$dbcount, p.adj="b")
plot(lmfit)
glmfit = glm(frac_median ~ dbcount, family=Gamma, data = lognormdata)
summary(glmfit)
anova(glmfit, test = "Chisq")
plot(glmfit)

fracmed1 = lm(frac_median ~ dbcount*distribution, data=combined)
summary(fracmed1)
fracmed2 =  lm(frac_median ~ dbcount + distribution, data=combined)
summary(fracmed2)
## TukeyHSD(a2, "distribution")# did not work
anova(fracmed1, fracmed2, test="LRT")
#Insignificant interaction

## summary(fracmed2)
## library(multcomp)
## summary(glht(fracmed2, mcp(distribution="Tukey")))

fraciqr1 = lm(frac_iqr ~ dbcount + distribution + dbcount*c(distribution), data=combined)
summary(fraciqr1)
fraciqr2 =  lm(frac_iqr ~ dbcount + distribution , data=combined)
summary(fraciqr2)
## TukeyHSD(a2, "distribution")# did not work
anova(fraciqr1, fraciqr2, test="LRT")
#Insignificant interaction

############################################
############################################
## Analyze inter burst intervals
############################################
############################################
ibinorm.lmfit = lm(ibi_median ~ dbcount, data = normdata)
summary(ibinorm.lmfit)
anova(ibinorm.lmfit, test = "Chisq")
plot(ibinorm.lmfit)


## ibimed1 = glm(ibi_median ~ dbcount + c(distribution) + dbcount*c(distribution), family=Gamma, data=combined)
ibimed1 = glm(ibi_median~ dbcount + distribution + dbcount*c(distribution), data=combined)
summary(ibimed1)
## ibimed2 =  glm(ibi_median ~ dbcount + c(distribution) , family=Gamma, data=combined)
ibimed2 =  lm(ibi_median~ dbcount + distribution , data=combined)
summary(ibimed2)
## lm.ibi.median= aov(ibi_median ~ dbcount + c(distribution) , data=combined)
## TukeyHSD(lm.ibi.med, "distribution")# did not work
anova(ibimed1, ibimed2, test="LRT")
#Interaction insignificant
#IBI - not significant on distribution, only over dbcount
## anova(ibimed2, test = "Chisq")
anova(ibimed2)

## Compare pairwise using KS test
dbcounts <- unique(normdata$dbcount)
for (n in dbcounts){
    ngrp = normdata[normdata$dbcount == n,]
    lngrp = lognormdata[lognormdata$dbcount == n,]
    kst = ks.test(ngrp$frac_median, lngrp$frac_median)
    print(n)
    print(kst)
}
ks.test(normdata[normdata$dbcount == 30,]$frac_median, lognormdata[lognormdata$dbcount == 30,]$frac_median)
ks.test(normdata[normdata$dbcount == 40,]$frac_median, lognormdata[lognormdata$dbcount == 40,]$frac_median)
ks.test(normdata[normdata$dbcount == 50,]$frac_median, lognormdata[lognormdata$dbcount == 50,]$frac_median)
ks.test(normdata[normdata$dbcount == 60,]$frac_median, lognormdata[lognormdata$dbcount == 60,]$frac_median)
ks.test(normdata[normdata$dbcount == 70,]$frac_median, lognormdata[lognormdata$dbcount == 70,]$frac_median)
ks.test(normdata[normdata$dbcount == 80,]$frac_median, lognormdata[lognormdata$dbcount == 80,]$frac_median)

for (n in dbcounts){
    ngrp = normdata[normdata$dbcount == n,]
    lngrp = lognormdata[lognormdata$dbcount == n,]
    kst = ks.test(ngrp$ibi_median, lngrp$ibi_median)
    print(n)
    print(kst$p.value)
}

ks.test(normdata[normdata$dbcount == 30,]$ibi_median, lognormdata[lognormdata$dbcount == 30,]$ibi_median)
ks.test(normdata[normdata$dbcount == 40,]$ibi_median, lognormdata[lognormdata$dbcount == 40,]$ibi_median)
ks.test(normdata[normdata$dbcount == 50,]$ibi_median, lognormdata[lognormdata$dbcount == 50,]$ibi_median)
ks.test(normdata[normdata$dbcount == 60,]$ibi_median, lognormdata[lognormdata$dbcount == 60,]$ibi_median)
ks.test(normdata[normdata$dbcount == 70,]$ibi_median, lognormdata[lognormdata$dbcount == 70,]$ibi_median)
ks.test(normdata[normdata$dbcount == 80,]$ibi_median, lognormdata[lognormdata$dbcount == 80,]$ibi_median)


sem.frac.fit =  lm(frac_sem ~ dbcount * distribution , data=combined)
summary(sem.frac.fit)
ggplot(normdata, aes(x=dbcount, y=frac_sem)) +geom_point(shape=19) + stat_smooth(method=lm)
ggplot(lognormdata, aes(x=dbcount, y=frac_sem)) +geom_point(shape=19) + stat_smooth(method=lm)
