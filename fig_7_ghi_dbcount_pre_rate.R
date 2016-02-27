library(ggplot2)
library(viridis)
normdata.ss = read.csv('norm_prepost_rates_SpinyStellate_20.0ms_window.csv')
myplot = ggplot(normdata.ss, aes(x=dbcount, y=premean)) +
    geom_point(shape=19) +
    xlab("# of basket cells") + ylab("pre-stimulus firing rate") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))  + ggtitle("spiny stellate") + coord_cartesian(ylim=c(-2, 70))
ggsave(file="figures/fig_7G_dbcount_pre_spiking_SS_20.0ms_window.svg", plot=myplot, width=2, height=2)
ss.dbcount.pre.lm = lm('premean ~ dbcount', data=normdata.ss)
summary(ss.dbcount.pre.lm)
ss.dbcount.post.lm = lm('postmean ~ dbcount', data=normdata.ss)
summary(ss.dbcount.post.lm)
##***** This is part of the text
# Compute Pearson's product moment correlation
cor.test(normdata.ss$dbcount, normdata.ss$premean)
cor.test(normdata.ss$dbcount, normdata.ss$postmean)
##***** This is part of the text

normdata.db = read.csv('norm_prepost_rates_DeepBasket_20.0ms_window.csv')
## myplot = ggplot(normdata.db, aes(x=dbcount, y=premean)) +
##     geom_point(shape=19) +
##     xlab("# of basket cells") + ylab("pre-stimulus firing rate") +
##     geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
##                                      panel.grid.major=element_blank(),
##                                      panel.grid.minor=element_blank(),
##                                      panel.background=element_blank(),
##                                      axis.title=element_text(family = "sans", face="plain", size=10),
##                                      legend.title=element_text(family = "sans", face="plain", size=10),
##                                      legend.text=element_text(family = "sans", face="plain", size=10))  + ggtitle("basket") + coord_cartesian(ylim=c(-2, 40))
## ggsave(file="figures/Figure_7H_dbcount_pre_spiking_DB_20.0ms_window.svg", plot=myplot, width=2, height=2)

db.dbcount.pre.lm = lm('premean ~ dbcount', data=normdata.db)
summary(db.dbcount.pre.lm)
##***** This is part of the text
# Compute Pearson's product moment correlation
cor.test(normdata.db$dbcount, normdata.db$premean)
cor.test(normdata.db$dbcount, normdata.db$postmean)

##***** This is part of the text

normdata.lts = read.csv('norm_prepost_rates_DeepLTS_20.0ms_window.csv')
## myplot = ggplot(normdata.lts, aes(x=dbcount, y=premean)) +
##     geom_point(shape=19) +
##     xlab("# of basket cells") + ylab("pre-stimulus firing rate") +
##     geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
##                                      panel.grid.major=element_blank(),
##                                      panel.grid.minor=element_blank(),
##                                      panel.background=element_blank(),
##                                      axis.title=element_text(family = "sans", face="plain", size=10),
##                                      legend.title=element_text(family = "sans", face="plain", size=10),
##                                      legend.text=element_text(family = "sans", face="plain", size=10))  + ggtitle("LTS") + coord_cartesian(ylim=c(-2, 30))
## ggsave(file="figures/Figure_7I_dbcount_pre_spiking_LTS_20.0ms_window.svg", plot=myplot, width=2, height=2)
lts.dbcount.pre.lm = lm('premean ~ dbcount', data=normdata.lts)
summary(lts.dbcount.pre.lm)
##***** This is part of the text
# Compute Pearson's product moment correlation
cor.test(normdata.lts$dbcount, normdata.lts$premean)
cor.test(normdata.lts$dbcount, normdata.lts$postmean)
##***** This is part of the text

## Plot the coefficient of variation as a measure of dispersal of PSTH
## height
## ** within each simulation
normdata.ss$cv.biased = normdata.ss$poststd/normdata.ss$postmean
normdata.ss$cv.unbiased = (1+1/(4.0 * normdata.ss$nstim)) * normdata.ss$cv.biased
myplot = ggplot(normdata.ss, aes(x=dbcount, y=cv.biased)) +
    geom_point(shape=19) +
    xlab("# of basket cells") + ylab("CV within network") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))
ggsave(file="figures/Figure_7H_dbcount_post_rate_cv_SS_20.0ms_window_biased.svg", plot=myplot, width=2, height=2)
myplot = ggplot(normdata.ss, aes(x=dbcount, y=cv.unbiased)) +
    geom_point(shape=19) +
    xlab("# of basket cells") + ylab("CV within network") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour='black'), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))
ggsave(file="figures/Figure_7H_dbcount_post_rate_cv_SS_20.0ms_window_unbiased.svg", plot=myplot, width=2, height=2)
## ** CV across simulations

cv <- function(x) sd(x)/mean(x)
normdata.ss.grpcv <- aggregate(normdata.ss$postmean, by=list(normdata.ss$dbcount), FUN = cv)
normdata.ss.grpcnt <- aggregate(normdata.ss$dbcount, by=list(normdata.ss$dbcount), FUN = length)
normdata.ss.grpcvcombined <- merge(normdata.ss.grpcv, normdata.ss.grpcnt, by="Group.1")
normdata.ss.grpcvcombined$unbiased = normdata.ss.grpcvcombined$x.x * (1+1/(4.0 * normdata.ss.grpcvcombined$x.y))
myplot = ggplot(normdata.ss.grpcv, aes(x=Group.1, y=x)) +
    geom_point(shape=19) +
    xlab("# of basket cells") + ylab("CV across networks") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour="black"), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))
ggsave(file="figures/Figure_7I_dbcount_post_rate_grpcv_SS_20.0ms_window_biased.svg", plot=myplot, width=2, height=2)

myplot = ggplot(normdata.ss.grpcvcombined, aes(x=Group.1, y=unbiased)) +
    geom_point(shape=19) +
    xlab("# of basket cells") + ylab("CV across networks") +
    geom_smooth(method="lm") + theme(axis.line=element_line(colour="black"), 
                                     panel.grid.major=element_blank(),
                                     panel.grid.minor=element_blank(),
                                     panel.background=element_blank(),
                                     axis.title=element_text(family = "sans", face="plain", size=10),
                                     legend.title=element_text(family = "sans", face="plain", size=10),
                                     legend.text=element_text(family = "sans", face="plain", size=10))
ggsave(file="figures/Figure_7I_dbcount_post_rate_grpcv_SS_20.0ms_window_unbiased.svg", plot=myplot, width=2, height=2)

