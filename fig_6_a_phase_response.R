library(ggplot2)
data <- read.csv("psth_phase_response.csv", header=TRUE, sep=",")
binom_plot = ggplot(data, aes(x=phase, y=psth_peak)) + geom_point(shape=1) +
    ## stat_smooth(se=FALSE, method="glm", family="binomial") +
    xlab("Stimulus delay (ms)") + ylab("Number of spikes") +
    theme(axis.line=element_line(colour="black"),
          panel.grid.major=element_blank(),
          panel.grid.minor=element_blank(),
          panel.background=element_blank(),
	  axis.text.x=element_text(family="sans", face="plain", colour="#000000", size=12),
	  axis.text.y=element_text(family="sans", face="plain", colour="#000000", size=12),
          axis.title=element_text(family = "sans", face="plain", size=12),
          legend.title=element_text(family = "sans", face="plain", size=12),
          legend.text=element_text(family = "sans", face="plain", size=12)) 
ggsave(file="figures/Figure_6_phase_response.svg", plot=binom_plot, width=6, height=3)


