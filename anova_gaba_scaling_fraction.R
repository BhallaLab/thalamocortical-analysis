library(ggplot2)
data <- read.csv("gaba_scale_ss_frac_cutoff_0.2_binwidth_0.5ms_lookahead_10.csv", header=TRUE, sep=",")
## qplot(normdata$dbcount, normdata$premean, geom=c("point", "smooth"), method="lm")

### First try linear regression
ss.lm = lm(formula = frac_med ~ gabascale, data=data)
summary(ss.lm)

### RESULTS:
## Call:
## lm(formula = frac_med ~ gabascale, data = data)

## Residuals:
##      Min       1Q   Median       3Q      Max 
## -0.30213 -0.05731  0.01170  0.07653  0.34421 

## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  1.36716    0.05358   25.52   <2e-16 ***
## gabascale   -0.73170    0.05812  -12.59   <2e-16 ***
## ---
## Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

## Residual standard error: 0.1191 on 103 degrees of freedom
##   (1 observation deleted due to missingness)
## Multiple R-squared:  0.6061,	Adjusted R-squared:  0.6023 
## F-statistic: 158.5 on 1 and 103 DF,  p-value: < 2.2e-16

## plot(ss.lm)

qplot(data$gabascale, data$frac_med, xlab="gaba scale", ylab="median sync frac", geom=c("point", "smooth"), method="lm")

### Try logistic regression - a cell will either fire or not fire
### (however the independece criterion is not true).
spiking <- round(data$frac_med*240)
nonspiking <- 240 - spiking
ss.logistic = glm(cbind(spiking, nonspiking )~ gabascale, data=data, family=binomial)
summary(ss.logistic)

### RESULTS:
## Call:
## glm(formula = cbind(spiking, nonspiking) ~ data$gabascale, family = binomial)

## Deviance Residuals: 
##     Min       1Q   Median       3Q      Max  
## -6.0006  -0.9905   0.1439   1.1290   5.2090  

## Coefficients:
##                Estimate Std. Error z value Pr(>|z|)    
## (Intercept)     0.59856    0.04496   13.31   <2e-16 ***
## data$gabascale -1.06904    0.05010  -21.34   <2e-16 ***
## ---
## Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

## (Dispersion parameter for binomial family taken to be 1)

##     Null deviance: 880.17  on 104  degrees of freedom
## Residual deviance: 419.74  on 103  degrees of freedom
##   (1 observation deleted due to missingness)
## AIC: 1097.1

## Number of Fisher Scoring iterations: 4

### Get back the coefficient in original scale - inverse of logit link 1/(1+1/exp(x))
1/(1+1/exp(coef(ss.logistic)))
## plot(data$gabascale, spiking)
### Lost here: http://plantecology.syr.edu/fridley/bio793/glm.html
## logistic.pred <- predict(ss.logistic, list(gabascale=gabascale), type="response")
## lines(predict(ss.logistic, list(gabascale=gabascale), type="response"), lwd=2, col="orange")
## anova(ss.lm, ss.logistic,test="Chisq")

### Plot the data with fitted model - checked with statsmodels - but could not produce the confidence interval
png("gabascale_binomial_fit.png", width=400, height=300)
binom_plot <- ggplot(data, aes(x=gabascale, y=frac_med)) + xlab("GABA scale") + ylab("Median fraction") + geom_point(shape=19) + geom_smooth(method="glm", family="binomial")
par(new=F)
binom_plot + theme(panel.grid.major=element_blank(), panel.grid.minor=element_blank(), panel.background=element_blank())
dev.off()




qplot(log(data$gabascale),log(data$frac_mean), xlab="gaba scale", ylab="sync frac", geom=c("point", "smooth"), method="lm")

fligner.test(frac_med ~ gabascale, data = data)
fligner.test(frac_mean ~ gabascale, data = data)
##Nonhomogeneous variance
oneway.test(frac_med ~ gabascale, data = data)
oneway.test(frac_mean ~ gabascale, data = data)

fit = glm(frac_mean ~ gabascale, family=Gamma, data=data)
summary(fit)
### Results:
## Call:
## glm(formula = frac_mean ~ gabascale, family = Gamma, data = data)

## Deviance Residuals: 
##      Min        1Q    Median        3Q       Max  
## -0.72497  -0.08795   0.01685   0.10320   0.45048  

## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)   0.1776     0.1031   1.723    0.088 .  
## gabascale     1.4388     0.1224  11.759   <2e-16 ***
## ---
## Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

## (Dispersion parameter for Gamma family taken to be 0.03045981)

##     Null deviance: 7.7622  on 104  degrees of freedom
## Residual deviance: 3.4841  on 103  degrees of freedom
##   (1 observation deleted due to missingness)
## AIC: -133.65

ggplot(data, aes(x=gabascale, y=frac_med)) + geom_point() + geom_smooth(method="glm", family=Gamma)
### Binomial looks like best fit.

fit = lm(frac_med ~ gabascale, data=data)
summary(fit)
plot(fit)


fit = lm(formula = log(frac_mean) ~ log(gabascale), data=data)
summary(fit)
plot(fit)

