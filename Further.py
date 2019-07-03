
from functions import *
with open('clean.json') as json_file:  
    lines=json_file.readlines()
    lines=dictionary_array(lines)
with open('DowJones30.txt') as fh:
    com_nam=fh.readlines()
with open('dict.json') as json_file:  
    data = json.load(json_file)

pool = mp.Pool(processes=mp.cpu_count())
pro_nam=pool.map(remove_junk, (com_nam[j] for j in range(len(com_nam)) ))
pro_nam=pool.map(remove_stop_words,(pro_nam[j] for j in range(len(pro_nam)) ))
pro_nam=pool.map(get_lemmatized_text,(pro_nam[j] for j in range(len(pro_nam)) ))
print("Names are cleared")

(top_dict,index_dict)=get_top(20000,data)
print("got dictionary")

indices=index_matrix(pro_nam,lines)
fh=open("value.txt","w")
for i in range(len(indices)):
    matrix=subarray(lines,indices[i])
    values=sliding_window_tfidf(matrix,top_dict,index_dict,20)
    for j in values:
        fh.write(str(j))
        fh.write(" ")
    fh.write("\n")
fh.close()
