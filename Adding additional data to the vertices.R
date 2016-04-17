#######################################################################################################
#####################Adds in personal characteristics to the graph#####################################
#######################################################################################################
#Reads in the graph data

red<-read.graph("C:\\Users\\John\\Google Drive\\tweets\\leWebdata\\follows-eigenvector-powerpost2.graphml", format="graphml")

#deletes the person who followed a lot of people before the event and then unfollowed them afterwards

red<-delete.vertices(red,which(V(red)$name=="Richard Tolcher"))


#################reads in the data which has the personal characteristics########################
perschar<-read.csv("C:\\Users\\John\\Google Drive\\tweets\\leWebdata\\personalcharacteristics101214 (1).csv", header=TRUE)
################################################################################################
#Sorts out the Nationality coding, collapsing the smaller countries to Other
#makes sure the country is coded as a character
perschar$Nationality<-as.character(perschar$Nationality)

#A label for countries with fewer than 10 people in the dataset
Others<-c("Greece/Switzerland/Finland", "Argentina", "Australia","Austria", ""," ","Belarus","Finland", "Brazil", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "French/Iranian","Holland", "Hungary","Lithuania","Malaysia", "Martinique","Mexican", "N/A","New Zealand","Norway", "Pakistan","Poland" ,"Portugal","Romania ", "Russia","Saudi Arabia","Serbia", "Singapore","Ukraine", "US/UK", "Slovakia", "South Africa", "Sweden", "Switzerland", "Ireland","India", "Israel","Turkey","Lebanon" ,"Japan", "Kazakhstan", "Latvia", "Greece", "Mexico")


#Sets countries in the above list to Other
perschar$Nationality<-ifelse((perschar$Nationality %in% as.vector(Others)),"Other", perschar$Nationality)


#sorts out the UK variable and Romania
perschar$Nationality<-ifelse(perschar$Nationality=="Uk","UK", perschar$Nationality)
perschar$Nationality<-ifelse(perschar$Nationality=="Romania","Other", perschar$Nationality)
                           

################################################################################################

#Creates an extra id variable to check it is matching correctly
V(red)$idcheck<-as.character(perschar$twitteruserid[match(V(red)$id,perschar$twitteruserid)])

#Mactches the vertices with the occupation info

V(red)$OT<-as.character(perschar$OT[match(V(red)$id, perschar$twitteruserid)])

#Matches the vertices with the industry info

V(red)$Industry<-as.character(perschar$Industryshort[match(V(red)$id, perschar$twitteruserid)])


#Matches the vertices with the Nationality information

V(red)$Nationality<-as.character(perschar$Nationality[match(V(red)$id, perschar$twitteruserid)])


#Matches the vertices with the Academic background information

V(red)$Academic.background<-as.character(perschar$Academic.background[match(V(red)$id, perschar$twitteruserid)])


#Writes the full network to the directory
write.graph(red,"C:\\Users\\John\\Google Drive\\tweets\\Networks for Juan\\fullnetwork.graphml",format=c("graphml") ) 

######################################
#Code that selects all the new edges

pre<-delete.edges(red,which(E(red)$pre=="false" ))

#creates the network which has only post-event connections in it i.e. deleted edges where post is false
post<-delete.edges(red,which(E(red)$post=="false" ))

newcon<-graph.difference(post,pre)
ecount(newcon)
                  
#Writes the graph to the directory


write.graph(newcon,"C:\\Users\\John\\Google Drive\\tweets\\Networks for Juan\\newconnection.graphml",format=c("graphml") ) 
####################################
#Selects all the new reciprocal edges (inc of consolicated )

newrec<-delete.edges(post, which(is.mutual(post, es = E(post))=="FALSE"))

oldrec<-delete.edges(pre, which(is.mutual(pre, es = E(pre))=="FALSE"))

newrec<-graph.difference(newrec,oldrec)
ecount(newrec)

#Writes the graph to the directory
write.graph(newrec ,"C:\\Users\\John\\Google Drive\\tweets\\Networks for Juan\\newrecconnection.graphml",format=c("graphml") ) 
#######

newrec2<-delete.vertices(newrec, which(degree(newrec)=="0"))


#Adds in the new data as an attribute

V(r)$Nationality<-as.character(perschar$Nationality[match(V(red)$id, perschar$twitteruserid)])













                