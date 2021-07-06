library(readr)
library(janitor)

## RY: import raw
ProQuestDocuments_parsed <- read_csv("~/Desktop/ProQuestDocuments_parsed.csv")
## AGG: import raw from SESYNC server
ProQuestDocuments_parsed<-read.csv("/nfs/mariculture-data/Text_Parser/data/ProQuestDocuments_parsed.csv")


#rename
articles<-ProQuestDocuments_parsed%>%
  clean_names()

dupe_title<-articles%>%get_dupes(title)%>%rename(dupe_title=dupe_count)%>%select(title)%>%unique()%>%mutate(dupe_title_id=row_number())
dupe_fulltext<-articles%>%get_dupes(full_text)%>%rename(dupe_ft=dupe_count)%>%select(full_text)%>%unique()%>%mutate(dupe_ft_id=row_number())

article2<-left_join(articles, dupe_title)%>%
  left_join(., dupe_fulltext)

article3<-article2%>%mutate(
  id=row_number()+1000
)

write.csv(article3, "article3.csv")

##testing
