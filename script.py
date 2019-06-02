#importing libraries
#SimpleJSON is better for loading this up
import simplejson as json
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#Reading the input files.
#2014.json file has few lines not parseable as json.
fh=open("2014.json","r")
lines=fh.readlines()
fh.close()
#This file contains the ones which are not parseable made parseable.
fh=open("cleaned.json","r")
clean=fh.readlines()
fh.close()
print("Read")
#finished reading in the files, now to parse.
url=[]
dop=[]
title=[]
text=[]
j=0
for i in range(len(lines)):
    try:
        parsed_lines=(json.loads(lines[i]))
        url.append(parsed_lines["url"])
        title.append(parsed_lines["title"])
        dop.append(parsed_lines["dop"])
        temp=parsed_lines["text"].lower()
        text.append(temp)
    except:
        parsed_lines=(json.loads(clean[j]))
        url.append(parsed_lines["url"])
        title.append(parsed_lines["title"])
        dop.append(parsed_lines["dop"])
        temp=parsed_lines["text"].lower()
        text.append(temp)
        j=j+1
print("Parsing finished!")
#Clearing of some memeory?
lines=[]
#Creating a dictionary the starting points of each date.
start_position={"20140101":0}
end_position={}
for i in range(1,len(dop)):
    temp1= (dop[i-1].split(" "))[0]
    temp2= (dop[i].split(" "))[0]
    if(temp1!=temp2):
        end_position[temp1]=i-1
        start_position[temp2]=i
end_position[temp2]=len(dop)-1
print("Dictionary created")
# set a start, end date and news you want to compare
print("Enter the date from which you want to start comparing")
print("The format should be YYYYMMDD")
start_date=str(input())
print("Enter the date till which you want to compare, the date is not included.")
print("The format should be YYYYMMDD")
end_date=str(input())
print("Specify a news article you want to compare, enter a number between %d and %d", (start_position[str(end_date)], end_position[str(end_date)]))
nn=input()

def tfidf(s,e,n):
    vectorizer = CountVectorizer()
    tempo=text[start_position[s]:start_position[e]]
    tempo=tempo+[text[n]]
    x = vectorizer.fit_transform(tempo)
    t=x.toarray()
    v=t[-1]
    transformer = TfidfTransformer(smooth_idf=False)
    x = transformer.fit_transform(t[:-1])
    mat=x.toarray()
    for i in range()
    return (x.toarray(),t[-1])

(mat,v)=tfidf(start_date,end_date,nn)

