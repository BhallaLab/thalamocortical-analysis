library(ggplot2)
data <- read.csv("norm_syncspike_stats_cutoff_0.2_binwidth_5.0ms_lookahead_10.csv", header=TRUE, sep=",")

### Plot the data with fitted model

binom_plot <- ggplot(data, aes(x=dbcount, y=ibi_median)) +
    geom_point(shape=1) + stat_smooth(method="lm", se=FALSE) +
    xlab("Basket cells") + ylab("Median interval (s)") +
    theme(axis.line=element_line(colour="black"),
          panel.grid.major=element_blank(),
          panel.grid.minor=element_blank(),
          panel.background=element_blank(),
	  axis.text.x=element_text(family="sans", face="plain", colour="#000000", size=12),
	  axis.text.y=element_text(family="sans", face="plain", colour="#000000", size=12),
          axis.title=element_text(family = "sans", face="plain", size=12),
          legend.title=element_text(family = "sans", face="plain", size=12),
          legend.text=element_text(family = "sans", face="plain", size=12)) +
	  ylim(0, 2.0)
ggsave(file="figures/Figure_5E_ibi_norm.svg", plot=binom_plot, width=3, height=3)


