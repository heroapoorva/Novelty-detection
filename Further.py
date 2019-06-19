
from functions.py import *
with open('clean.json') as json_file:  
    lines=json_file.readlines()
    lines=dictionary_array(lines)
with open('DowJones30.txt') as fh:
    com_nam=fh.readlines()

pool = mp.Pool(processes=mp.cpu_count())
english_stop_words = stopwords.words('english')
pro_nam=pool.map(remove_junk, (com_nam[j] for j in range(len(com_nam)) ))
pro_nam=pool.map(remove_stop_words,(pro_nam[j] for j in range(len(pro_nam)) ))
pro_nam=pool.map(get_lemmatized_text,(pro_nam[j] for j in range(len(pro_nam)) ))
matrix=index_matrix(com_nam,pro_nam)

