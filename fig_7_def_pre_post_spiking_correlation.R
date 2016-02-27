library(ggplot2)
library(viridis)
normdata.ss = read.csv('norm_prepost_rates_SpinyStellate_20.0ms_window.csv')
myplot = ggplot(normdata.ss, aes(x=log(premean), y=log(postmean))) +
    geom_point(shape=19, aes(colour=dbcount)) +
        scale_color_viridis(name="basket cells") +
       xlab("log(pre-stimulus firing rate)") + ylab("log(post-stimulus firing rate)") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))  + ggtitle("Spiny stellate cell population") + coord_cartesian(ylim=c(0, 5), xlim=c(-2, 5))
ggsave(file="figures/Figure_7D_pre_post_spiking_SS_20.0ms_window.svg", plot=myplot, width=3, height=2)
ss.prepost.lm = lm('log(postmean) ~ log(premean)', data=normdata.ss)
summary(ss.prepost.lm)
##***** This is part of the text
# Compute Pearson's product moment correlation
cor.test(log(normdata.ss$premean), log(normdata.ss$postmean))
##***** This is part of the text


normdata.db = read.csv('norm_prepost_rates_DeepBasket_20.0ms_window.csv')
myplot = ggplot(normdata.db, aes(x=log(premean), y=log(postmean))) +
    geom_point(shape=19, aes(colour=dbcount)) +
        scale_color_viridis(name="basket cells") +
       xlab("log(pre-stimulus firing rate)") + ylab("log(post-stimulus firing rate)") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'),
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10)) + ggtitle("Basket cell population")  + coord_cartesian(ylim=c(0, 5), xlim=c(1, 4))
ggsave(file="figures/Figure_7E_pre_post_spiking_DB_20.0ms_window.svg", plot=myplot, width=3, height=2) 

db.prepost.lm = lm('log(postmean) ~ log(premean)', data=normdata.db)
summary(db.prepost.lm)

cor.test(log(normdata.db$premean), log(normdata.db$postmean))

myplot = ggplot(normdata.db, aes(x=log(premean), y=log(postmean))) +
    geom_point(shape=19, aes(colour=dbcount)) +
        scale_color_viridis(name="basket cells") +
       xlab("log(pre-stimulus firing rate)") + ylab("log(post-stimulus firing rate)") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'),
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10)) + ggtitle("Basket cell population")


normdata.lts = read.csv('norm_prepost_rates_DeepLTS_20.0ms_window.csv')
## Problem - some values are 0 - so log does not work
## Hence remove the 0 entries
cleaned = subset(normdata.lts, normdata.lts$premean > 0)
myplot = ggplot(cleaned, aes(x=log(premean), y=log(postmean))) +
    geom_point(shape=19, aes(colour=dbcount)) +
        scale_color_viridis(name="basket cells") +
       xlab("log(pre-stimulus firing rate)") + ylab("log(post-stimulus firing rate)") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'),
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10)) + ggtitle("LTS population") ## + coord_cartesian(ylim=c(0, 5), xlim=c(-2, 5))
ggsave(file="figures/Figure_7F_pre_post_spiking_LTS_20.0ms_window.svg", plot=myplot, width=3, height=2)

lts.prepost.lm = lm('log(postmean) ~ log(premean)', data=cleaned)
summary(lts.prepost.lm)

cor.test(log(cleaned$premean), log(cleaned$postmean))


