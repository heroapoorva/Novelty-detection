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
print("Got dictionary")

indices=index_matrix(pro_nam,lines)
print("Got indices")

y=[]
for i in range(len(indices)):
    for j in range(len(indices[i])):
        y.append(i)
y=np.asarray(y)
print("Got y")

indices=flatten_2d(indices)
X=frequency_matrix(subarray(lines,indices), top_dict,index_dict)
print("Got X")

clf = naive_bayes(len(pro_nam))
clf = clf.fit(X, y)
Print("Fitting Done")
answers=clf.predict([frequency_vector(lines[0]["text"], top_dict, index_dict)])
print(answers)
