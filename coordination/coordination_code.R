library(dplyr)
outcometable<-select(sb_flat_dec28_types,newId,message,subscriberCount.x,url.x,actual.likeCount,actual.shareCount,actual.commentCount,date2,link,name.x)

outcometable<-merge(outcometable,topaccounts_formerging_dec28,by="name.x",all.x = TRUE)
outcometable<-outcometable[!duplicated(outcometable$newId),]
##https://medium.com/swlh/detecting-coordination-in-disinformation-campaigns-7e9fa4ca44f3

contunique<-as.data.frame(unique(outcometable$message))
library(dplyr)     # load the package in your work environment
outcometable %>%
  group_by(message) %>%      # group your data based on the variable Rating
  arrange(desc(url.x)) %>%     # order in descending order the variable One_Year_Return
  slice(1)    # extract the first row (the observation with the highest return of each group)


content_shared<-outcometable %>% mutate(message)%>% select(name.x,url.x,message)
content_shared$count<-1
content_shared<-content_shared[!is.na(content_shared$message),]
#library(stringi)
#content_shared$message2<-stri_sub(content_shared$message,1,200)

content_shared_agg<-aggregate(content_shared$count,by=list(content_shared$message),FUN=sum)
content_shared_agg5<-content_shared_agg[content_shared_agg$x>=5,]


head(content_shared)
names(content_shared)<-c("name","url","message")

names(content_shared_agg5)<-c("message","counts")
content_shared_agg5<-content_shared_agg5[!(content_shared_agg5$message %in% "'"),]

library(dplyr)
library(tidyr)
library(widyr)
library(stringr)

content_correlations <- content_shared %>% semi_join(content_shared_agg5) %>%
add_count(name.x,message) %>% filter(n>5)%>% pairwise_cor(name.x,message,sort=T)

##keep all the labeled accounts too
labeled_accounts<-as.data.frame(unique(outcometable$name[!is.na(outcometable$type)]))

rm(content_corr_pt25)
content_corr_pt2<-content_correlations[content_correlations$correlation>0.2,]
content_corr_spl1<-content_correlations[content_correlations$item1 %in% topaccounts_dec28$name,]
content_corr_spl2<-content_correlations[content_correlations$item2 %in% topaccounts_dec28$name,]
content_corr_spl<-rbind(content_corr_spl1,content_corr_spl2)
content_corr_spl<-content_corr_spl[content_corr_spl$correlation>.1,]

content_common_all<-rbind(content_corr_pt2,content_corr_spl)
### write
data.table::fwrite(content_common_all,"content_network_correlatedpt5.csv",row.names=FALSE)


domains_shared<-outcometable %>% mutate(domain=sapply(link,urltools::domain))%>% select(name.x,url.x,domain)
domain_counts<-domains_shared %>% filter(!is.na(domain)) %>% 
  filter(!str_detect(domain,"facebook|yout|twitt|bit.ly|t.co|owl.li|buff.ly|ow.ly|wp.me|dlvr.it"))%>%
  count(domain,sort="T")%>%
  filter(n>20)


domain_correlations <- domains_shared %>% semi_join(domain_counts) %>%
  add_count(name.x,domain) %>% filter(n>5)%>% pairwise_cor(name.x,domain,sort=T)


domain_corr_pt5<-domain_correlations[domain_correlations$correlation>.5,]
#1143 users



data.table::fwrite(domain_corr_pt5,"domain_network_correlatedpt5.csv",row.names=FALSE)

