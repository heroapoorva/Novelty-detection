import simplejson as json
import numpy as np

print("Imports done")
def max_key(d1):  
     v=list(d1.values())
     k=list(d1.keys())
     return k[v.index(max(v))]
def get_top(n,d):
    newd={}
    index={}
    for i in range(n):
        temp=max_key(d)
        newd[temp]=d[temp]
        index[temp]=i
        d.pop(temp, None)
    return(newd,index)
def dictionary_array(t):
    for i in range(len(t)):
        t[i]=(json.loads(t[i]))
    return(t)
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
    temp_array=[]
    for i in range(len(newd.keys())):
        temp_array.append(0)
    for word in temp_text:
        if(word in newd.keys()):
            temp_array[index[word]]=temp_array[index[word]]+1
    return (temp_array)
def create_matrix(start_point,end_point,l,td,ind):
    matrix=[]
    for i in range(start_point,end_point):
        to_append=create_vector(l[i]["text"],td,ind)
        matrix.append(to_append)
    return matrix
def tfidf(s,e,n,l,td,ind,sp,ep):
    mat=create_matrix(sp[s],sp[e],l,td,ind)
    v=create_vector(l[n]["text"],td,ind)
    max_prod=0
    max_index=0
    for i in range(len(mat)-1):
        if(max_prod< np.dot(v,mat[i])):
            print(max_prod,i)
            max_prod=np.dot(v,mat[i])
            max_index=i
    return (mat,max_prod,i+sp[s])
def repeat_tfidf(mat,l,td,ind,n,spsd):
    v=create_vector(l[n]["text"],td,ind)
    max_prod=0
    max_index=0
    for i in range(len(mat)-1):
        if(max_prod< np.dot(v,mat[i])):
            print(max_prod,i)
            max_prod=np.dot(v,mat[i])
            max_index=i
    return (max_prod,i+spsd)

with open('clean.json') as json_file:  
    lines=json_file.readlines()
with open('dict.json') as json_file:  
    data = json.load(json_file)
print("Read the news files and the dictionary")
(top_dict,indices)=get_top(200,data)
print("got dictionary")
dictionary_array(lines)
print("Parsing finished!")
(start_position,end_position)=date_dictionary(lines)
print("Dictionary created")
print("Enter the date from which you want to start comparing")
print("The format should be YYYYMMDD")
start_date=str(input())
print("Enter the date till which you want to compare, the date is not included.")
print("The format should be YYYYMMDD")
end_date=str(input())
print("Specify a news article you want to compare, enter a number between %d and %d", (start_position[str(end_date)], end_position[str(end_date)]))
nn=input()
(matrix,temp1,temp2)=tfidf(start_date,end_date,start_position[str(end_date)],lines,top_dict,indices,start_position,end_position)
for i in range(start_position[str(end_date)]+1, end_position[str(end_date)]):
    repeat_tfidf(matrix,lines,top_dict,indices,i,start_position[start_date])
