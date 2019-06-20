#!/usr/bin/python
# -*- coding: utf-8 -*-

import simplejson as json
import numpy as np
import collections
import multiprocessing as mp
from joblib import Parallel, delayed
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

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
    output=''
    space_characters=["1","2","3","4","5","6","7","8","9","0","~","`","!","@","#","$","%","^",
    "&","*","(",")","_","-","+","=","{","}","[","]","|","\\",":",";","\"","'",",","<",".",">","/","?",]
    for i in range(len(t)):
        if(t[i] in space_characters):
            output=output+" "
        else:
            output=output+t[i].lower()
    output="".join([x if ord(x) < 128 else '' for x in output])
    return output

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
        parsed_line=(json.loads(make_parseable(t)))
    parsed_line["text"]=remove_junk(parsed_line["text"])
    parsed_line["text"]=remove_stop_words(parsed_line["text"])
    parsed_line["text"]=get_lemmatized_text(parsed_line["text"])
    parsed_line["title"]=remove_junk(parsed_line["title"])
    parsed_line["title"]=remove_stop_words(parsed_line["title"])
    parsed_line["title"]=get_lemmatized_text(parsed_line["title"])
    return  (parsed_line)

def final_function(t):
    return(json.dumps(do_all(t)))

def get_top(n,d):
    newd={}
    index={}
    i=0
    for k,v in collections.Counter(d).most_common(n):
        newd[k]=v
        index[k]=i
        i=i+1
    return(newd,index)

def dictionary_array(t):
    pool = mp.Pool(processes=mp.cpu_count())
    new = pool.map(json.loads, (t[i] for i in range(len(t)) ))
    return(new)

def date_dictionary(t):
    start_position={"20140101":0}
    end_position={}
    for i in range(1,len(t)):
        temp1= (t[i-1]["dop"].split(" "))[0]
        temp2= (t[i]["dop"].split(" "))[0]
        if(temp1!=temp2):
            end_position[temp1]=i-1
            start_position[temp2]=i
    end_position[temp2]=len(t)-1
    return(start_position,end_position)

#Given a string and the 2 dictionaries, the function
def frequency_vector(t,newd,index):
    temp_text=t.split()
    temp_array=np.zeros(len(newd.keys()))
    for word in temp_text:
        try:
            temp_array[index[word]]=temp_array[index[word]]+1
        except:
            continue
    return (np.asarray(temp_array))

def tfidf_matrix(l,td,ind):
    matrix=[]
    for i in range(len(l)):
        matrix.append(0)
    for i in range(len(l)):
        to_append=frequency_vector(l[i]["text"],td,ind)
        matrix[i]=to_append
    return (matrix)

def tfidf(mat,l,td,ind,spsd):
    v=frequency_vector(l,td,ind)
    max_prod=0
    max_index=0
    for i in range(len(mat)-1):
        if(max_prod < np.dot(v,mat[i])):
            max_prod=np.dot(v,mat[i])
            max_index=i
    return (max_prod,max_index+spsd)

# Given 2 list of "pro_nam" of strings and "lines" of dictionaries. The 
# function returns a 2D array ith array contains indices of occurances of
# com_nam[i] in lines['title'].
def index_matrix(pro_nam,lines):
    pro_mat=[]
    for j in range(len(pro_nam)):
        pro_mat.append([])
    for j in range(len(pro_nam)):
        temp_array=pro_nam[j].split()
        for i in range(len(lines)):
            for k in temp_array:
                if(len(k)>1 and k in lines[i]['title']):
                    pro_mat[j].append(i)
                    break
    return pro_mat

# Given a list "l" and a list of indices "a". The function returns a subset of 
# "l" with the indices in "a".
def subarray(l,a):
    output=[]
    for i in range(len(a)):
        output.append(l[i])
    return (output)
    
# Sliding the window for TF-IDF.
def sliding_window_tfidf(mat, td, ind,size):
    output=[]
    matrix=tfidf_matrix(mat[:size],td, ind)
    for i in range(size,len(mat)):
        temp_array=frequency_vector(mat[i]["text"],td,ind)
        (sp,si)=tfidf(matrix,mat[i]["text"],td,ind,0)
        output.append(sp)
        matrix=matrix[1:]
        matrix.append(0)
        matrix[-1]=temp_array
    return output
