#!/usr/bin/python
# -*- coding: utf-8 -*-

import simplejson as json
import numpy as np
import collections
from collections import Counter
import multiprocessing as mp
from joblib import Parallel, delayed
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from math import log
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

#Given a string, a top words dictionary and the inverse
# index dictionary. The function returns a frequency vector
def frequency_vector(t,newd,index):
    temp_text=t.split()
    temp_array=np.zeros(len(newd.keys()))
    for word in temp_text:
        try:
            temp_array[index[word]]=temp_array[index[word]]+1
        except:
            continue
    return (np.asarray(temp_array))

# Takes in input a list of dictionaries, a top words dictionary and the inverse
# index dictionary. The function return a matrix of frequency matrix
def frequency_matrix(l,td,ind):
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
# pro_nam[i] in lines['title'].
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
    
# Sliding the window for TF-IDF. Takes in input a 
def sliding_window_tfidf(mat, td, ind,size):
    output=[]
    matrix=frequency_matrix(mat[:size],td, ind)
    for i in range(size,len(mat)):
        (sp,si)=tfidf(matrix,mat[i]["text"],td,ind,0)
        output.append(sp)
        matrix=matrix[1:]
        matrix.append(0)
        matrix[-1]=frequency_vector(mat[i]["text"],td,ind)
    return output

# Given a 2d array into a 1d array row wise. 
def flatten_2d(a):
    output=[]
    for i in a:
        output=output+i
    return output
# A Naive Bayes Classifier, the labels must be intergers and so must the vector
# Having multiple values don't matter
class naive_bayes:
    def __init__(self,n):
        self.prior = {}
        self.categories = n
        self.label_counts = Counter()
        for i in range(n):
            self.label_counts[i] = 0
        self.is_fitted = False
        self.probability_matrix=[[]]
        
    def fit(self, X, y):
        self.probability_matrix = np.zeros(( self.categories , len(X[0]) ))
        for i, example in enumerate(X):
            label=y[i]
            self.label_counts[label] += 1
            for j in range(len(example)):
               if(example[j] != 0):
                    self.probability_matrix[label,j] += 1
        for i in range(len(self.probability_matrix)):
            if(self.label_counts[i] != 0):
                self.probability_matrix[i] /= self.label_counts[i]        
        total_examples = len(y)
        for label in set(y):
            self.prior[label] = float(self.label_counts[label]) / total_examples
        self.is_fitted = True
        return self
    
    def predict(self, test_set):
        self._check_fitted()
        predictions = []
        for i in range(len(test_set)):
            result = self.predict_record(test_set[i])
            predictions.append(result)
        return predictions
    
    def predict_record(self, test_case):
        log_likelihood = {k: log(v) for k, v in self.prior.items()}
        for label in self.label_counts:
            for i in range(len(test_case)):
                if(test_case[i] != 0):
                    probability = self.probability_matrix[label,i]
                    try:
                        log_likelihood[label] += log(probability)
                    except:
                        continue
        return max(log_likelihood, key=log_likelihood.get)
    
    def _check_fitted(self):
        if not self.is_fitted:
            raise NotFittedError(self.__class__.__name__)
