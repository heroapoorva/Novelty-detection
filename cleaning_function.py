#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
import multiprocessing as mp
import sys

# The original news documents contain articles which are not json parseable.
# Simply check for url, title, dop and text files.
def make_parseable(t):
    output=""
    i=0
    seen=0
    while(i<len(t)):
        if(t[i]=='"'):
            if(t[i:i+8]=='"url": "'):
                output=output+ '"url": "'
                i=i+8
            elif(t[i:i+13]=='", "title": "'):
                output=output+'", "title": "'
                i=i+13
            elif(t[i:i+11]=='", "dop": "'):
                output=output+'", "dop": "'
                i=i+11
            elif(t[i:i+12]=='", "text": "'):
                output=output+'", "text": "'
                i=i+12
            elif(t[i:i+3]=='" }'):
                output=output+'" }'
                i=i+3
            else:
                i=i+1
        elif(t[i]=='\\'):
            i=i+1
        else:
            output=output+t[i]
            i=i+1
    return output

#removing random symbols
def remove_junk(t):
    utf=''
    utf="".join([x if ord(x) < 128 else ' ' for x in t.lower()])
    '''
    space_characters=["1","2","3","4","5","6","7","8","9","0","~","`","!","@","#","$","%","^",
    "&","*","(",")","_","-","+","=","{","}","[","]","|","\\",":",";","\"","'",",","<",".",">","/","?",]
    for i in range(len(t)):
        if(t[i] in space_characters):
            output=output+" "
        else:
            output=output+t[i].lower()
    '''
    return utf

#Removing stopwords
def remove_stop_words(t):
    english_stop_words = stopwords.words('english')
    return(' '.join([word for word in t.split() if word not in english_stop_words]))

#Lemmatization    
def get_lemmatized_text(t):
    lemmatizer = WordNetLemmatizer()
    return(' '.join([lemmatizer.lemmatize(word) for word in t.split()]))

#Running and printing in a new file
def do_all(t):
    try:
        parsed_line=(json.loads(t))
    except:
        temp = make_parseable(t)
        parsed_line=(json.loads(temp))
    parsed_line["text"]=remove_junk(parsed_line["text"])
#    parsed_line["text"]=remove_stop_words(parsed_line["text"])
#    parsed_line["text"]=get_lemmatized_text(parsed_line["text"])
    parsed_line["title"]=remove_junk(parsed_line["title"])
#    parsed_line["title"]=remove_stop_words(parsed_line["title"])
#    parsed_line["title"]=get_lemmatized_text(parsed_line["title"])
    return  (parsed_line)

def final_function(t):
    return(json.dumps(do_all(t)))
