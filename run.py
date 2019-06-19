import simplejson as json
import numpy as np
import collections
import multiprocessing as mp
from joblib import Parallel, delayed
print("Imports done")
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
def create_matrix(start_point,end_point,l,td,ind):
    matrix=[]
    for i in range(start_point,end_point):
        matrix.append(0)
    for i in range(start_point,end_point):
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

with open('clean.json') as json_file:  
    lines=json_file.readlines()
with open('dict.json') as json_file:  
    data = json.load(json_file)

print("Read the news files and the dictionary")
(top_dict,indices)=get_top(20000,data)
print("got dictionary")
lines=dictionary_array(lines)
print("Parsing finished!")
(start_position,end_position)=date_dictionary(lines)
print("Dictionary created")
start_date=str(input("Enter the date from which you want to start comparing\n The format should be YYYYMMDD.\n"))
start_date="20140101"
end_date=str(input("Enter the date till which you want to compare, the date is not included.\n The format should be YYYYMMDD.\n"))
print("Specify a news article you want to compare, enter a number between %d and %d", (start_position[str(end_date)], end_position[str(end_date)]))
nn=input()
matrix=create_matrix(start_position[start_date],start_position[end_date],lines,top_dict,indices)
print("Matrix created.")
for i in range(start_position[str(end_date)]+1, end_position[str(end_date)]):
    (sp, si) = tfidf(matrix, lines, top_dict, indices, i, start_position[start_date])
    print(si)
