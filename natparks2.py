import numpy as np
import pandas as pd
import re 
import matplotlib.pyplot as plt
import nltk

#Read in CSV of all films that contain content on National Parks 
df=pd.read_csv('parksfilms.csv')
df.head()

#Read in CSV of all parks and their respective states
dfparkslist = pd.read_csv('parkslist.csv')
dfparkslist.head()

#Clean up dataset
#remove all films where national parks appear only in the comments
df = df.drop(df[df.Notes.str.contains('only in comments', case=False, na=False)].index)  

#Create new dataframe for each National Park and the number of films it appears in
dfparktotals = pd.DataFrame()
#Determine how many times each park is covered in films (includes parks mentioned in the Name, Topics, or Description for each film). Is case insensitive.
for i in range(0, 59):
	parkname = dfparkslist.iloc[i][0]
	dfpark = df.loc[df.Name.str.contains(parkname, case=False, na=False) | df.Description.str.contains(parkname, case=False, na=False) | df.Topics.str.contains(parkname, case=False, na=False)]
	NumofParks = len(dfpark.index)
	if NumofParks != 0:
		#print out the name of each park and the number of films it appears in
		print(parkname + " National Park appears in " + str(NumofParks) + " films")
		#add a row to the dfparkstotal dataframe with the name of the park and the total number of films it appears in
		dfparktotals = dfparktotals.append({'Parkname': parkname, "Totalfilms": NumofParks}, ignore_index=True)
		

#Plot representation of National Parks
parknames = (dfparktotals['Parkname'][0], dfparktotals['Parkname'][1], dfparktotals['Parkname'][2], dfparktotals['Parkname'][3], dfparktotals['Parkname'][4], dfparktotals['Parkname'][5], dfparktotals['Parkname'][6], dfparktotals['Parkname'][7], dfparktotals['Parkname'][8], dfparktotals['Parkname'][9], dfparktotals['Parkname'][10], dfparktotals['Parkname'][11], dfparktotals['Parkname'][12], dfparktotals['Parkname'][13], dfparktotals['Parkname'][14], dfparktotals['Parkname'][15], dfparktotals['Parkname'][16])        
y_pos = np.arange(len(parknames))
totalsperpark = [dfparktotals['Totalfilms'][0], dfparktotals['Totalfilms'][1], dfparktotals['Totalfilms'][2], dfparktotals['Totalfilms'][3], dfparktotals['Totalfilms'][4], dfparktotals['Totalfilms'][5], dfparktotals['Totalfilms'][6], dfparktotals['Totalfilms'][7], dfparktotals['Totalfilms'][8], dfparktotals['Totalfilms'][9], dfparktotals['Totalfilms'][10], dfparktotals['Totalfilms'][11], dfparktotals['Totalfilms'][12], dfparktotals['Totalfilms'][13], dfparktotals['Totalfilms'][14], dfparktotals['Totalfilms'][15], dfparktotals['Totalfilms'][16]]

plt.barh(y_pos, totalsperpark, align='center')
plt.yticks(y_pos, parknames)
plt.xlabel('Representation of Park in Prelinger Archives')
plt.ylabel('National Park')
plt.title('National Parks appearing in Prelinger Archive films')
plt.show()

#Find the most common words in the topics list
#Create new empty list for topics
alltopics = list()
#Add all the topics to the empty list
for i in range(0, 54):
	topics = df.iloc[i][2]	
	alltopics.append(topics)
#Remove all instances of nan
filteredalltopics = [a for a in alltopics if str(a) != 'nan']

#Tokenize and run word frequency
from nltk.tokenize import word_tokenize
tokenizedtopics2 = [word_tokenize(i) for i in filteredalltopics]

#Make topics into a single list (rather than lists of lists)
finalalltopics = []
for sublist in tokenizedtopics2:
    for i in sublist:
        finalalltopics.append(i)
        
#Remove any single character words (e.g. punctuation)
for w in finalalltopics:
    if len(w) == 1:
        finalalltopics.remove(w)

#Calculate word frequency
from nltk import FreqDist
termfrequencyTopics = nltk.FreqDist(finalalltopics)


#Find the most common words in the descriptions
#Create new empty list for descriptions
alldescriptions = list()
#Add all the descriptions to the empty list
for i in range(0, 54):
	descriptions = df.iloc[i][3]
	alldescriptions.append(descriptions)
#Remove all instances of nan
filteredalldescriptions = [a for a in alldescriptions if str(a) != 'nan']

#Tokenize and run word frequency
tokenizeddescriptions = [word_tokenize(i) for i in filteredalldescriptions]

#Make topics into a single list (rather than lists of lists)
finalalldescriptions = []
for sublist in tokenizeddescriptions:
    for i in sublist:
        finalalldescriptions.append(i)
           
#Remove all stop words and any one or two character words (e.g. punctuation)
from nltk.corpus import stopwords    
for w in finalalldescriptions:
    if (len(w) == 1) | len(w) == 2  | (w in stopwords.words('english')):
        finalalldescriptions.remove(w)

#Calculate word frequency
termfrequencyDescriptions = nltk.FreqDist(finalalldescriptions)
