from dictionary_function import *

import collections
from collections import Counter
import numpy as np
from math import log

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
    
def frequency_vector(t,newd,index):
    
    '''
    Given a string, a top words dictionary and the inverse
    index dictionary. The function returns a normalized 
    frequency vector.
    '''
    temp_text=t.split()
    temp_array=np.zeros(len(newd.keys()))
    for word in temp_text:
        try:
            temp_array[index[word]]=temp_array[index[word]]+1
        except:
            continue
    try:
        temp_array = temp_array / (np.sum(temp_array))
    except:
        continue
    return (temp_array)

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
    
def idf_array(l):
    output = np.zeros(len(l[0]))
    for i in range(len(output)):
        try:
            output[i] = log( float(len(l)) / np.count_nonzero(l[:,i]))
        except:
            output[i] = 0
    return output

def read_input(f, a):
    output=[]
    fh = open(f,"r")
    for i, line in enumerate(fh):
        if(i in a):
            output.append(line)
    return output
    
def tfidf_matrix(l):
    return np.multiply(np.asarray(l),idf_array(l))
    
def novelty(mat,l,td,ind,spsd):
    v=frequency_vector(l,td,ind)
    max_prod=0
    max_index=0
    for i in range(len(mat)-1):
        if(max_prod < np.dot(v,mat[i])):
            max_prod = np.dot(v,mat[i])
            max_index = i
    return (max_prod, max_index+spsd)

# Sliding the window for TF-IDF. Takes in input a 
def sliding_window_tfidf(mat, td, ind,size):
    output=[]
    freq_matrix = frequency_matrix(mat[:size],td, ind)
    tf_idf_matrix = tfidf_matrix(freq_matrix)
    for i in range(size,len(mat)):
        (sp, si) = novelty(tf_idf_matrix,mat[i]["text"], td, ind, 0)
        output.append(sp)
        freq_matrix = freq_matrix[1:]
        freq_matrix.append(0)
        freq_matrix[-1] = frequency_vector(mat[i]["text"], td, ind)
        tf_idf_matrix = tfidf_matrix(freq_matrix)
    return output
