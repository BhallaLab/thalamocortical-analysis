library(ggplot2)
data <- read.csv("lognorm_syncspike_stats_cutoff_0.2_binwidth_5.0ms_lookahead_10.csv", header=TRUE, sep=",")

### Try logistic regression - a cell will either fire or not fire
### (however the independece criterion is not true).
spiking <- round(data$frac_median*240)
nonspiking <- 240 - spiking
ss.logistic = glm(cbind(spiking, nonspiking )~ dbcount, data=data, family=binomial)
summary(ss.logistic)
## ss.null <-  glm(cbind(spiking, nonspiking )~ 1, data=data, family=binomial)
## with(anova(ss.logistic, ss.null),pchisq(Deviance,Df,lower.tail=FALSE)[2])

## pchisq(deviance(ss.null)-deviance(ss.logistic), df.residual(ss.null)-df.residual(ss.logistic),lower.tail=FALSE)
### Get back the coefficient in original scale - inverse of logit link 1/(1+1/exp(x))
1/(1+1/exp(coef(ss.logistic)))
## plot(data$gabascale, spiking)
### Lost here: http://plantecology.syr.edu/fridley/bio793/glm.html
## logistic.pred <- predict(ss.logistic, list(gabascale=gabascale), type="response")
## lines(predict(ss.logistic, list(gabascale=gabascale), type="response"), lwd=2, col="orange")
## anova(ss.lm, ss.logistic,test="Chisq")

### Plot the data with fitted model

binom_plot <- ggplot(data, aes(x=dbcount, y=frac_median)) +
    geom_point(shape=1) + stat_smooth(se=FALSE, method="glm", family="binomial") +
    xlab("basket cells") + ylab("Median fraction") +
    theme(axis.line=element_line(colour="black"),
          panel.grid.major=element_blank(),
          panel.grid.minor=element_blank(),
          panel.background=element_blank(),
	  axis.text.x=element_text(family="sans", face="plain", colour="#000000", size=12),
	  axis.text.y=element_text(family="sans", face="plain", colour="#000000", size=12),
          axis.title=element_text(family = "sans", face="plain", size=12),
          legend.title=element_text(family = "sans", face="plain", size=12),
          legend.text=element_text(family = "sans", face="plain", size=12)) +
	  ylim(0, 1.0)
ggsave(file="figures/Figure_5D_syncfrac_lognorm.svg", plot=binom_plot, width=3, height=3)


