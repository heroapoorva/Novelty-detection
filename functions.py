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
def create_vector(t,newd,index):
    temp_text=t.split()
    temp_array=np.zeros(len(newd.keys()))
    for word in temp_text:
        try:
            temp_array[index[word]]=temp_array[index[word]]+1
        except:
            continue
    return (np.asarray(temp_array))
def create_matrix(l,td,ind):
    matrix=[]
    for i in range(len(l)):
        matrix.append(0)
    for i in range(len(l)):
        to_append=create_vector(l[i]["text"],td,ind)
        matrix[i]=to_append
    return (matrix)
def tfidf(mat,l,td,ind,n,spsd):
    v=create_vector(l[n]["text"],td,ind)
    max_prod=0
    max_index=0
    for i in range(len(mat)-1):
        if(max_prod < np.dot(v,mat[i])):
            max_prod=np.dot(v,mat[i])
            max_index=i
    return (max_prod,max_index+spsd)
def index_matrix(com_nam, pro_nam):
    pro_mat=[]
    for j in range(len(com_nam)):
        pro_mat.append([])
    for j in range(len(pro_nam)):
        temp_array=pro_nam[j].split()
        for i in range(len(lines)):
            for k in temp_array:
                if(len(k)>1 and k in lines[i]['title']):
                    pro_mat[j].append(i)
                    break
    return pro_mat
