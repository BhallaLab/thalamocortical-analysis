library(ggplot2)
normdata = read.csv('syncspikestats_norm_0.2_5.0ms.csv')
summary(normdata)
ggplot(normdata,aes(x=dbcnt,y=sem)) +  geom_point() +  geom_smooth(method="lm")
sem.fit = lm(sem ~ dbcnt, data=normdata)
summary(sem.fit)

