from novelty_function import *

# Given 2 list of "keywords" of strings and "lines" of dictionaries. The 
# function returns a 2D array ith array contains indices of occurances of
# pro_nam[i] in lines['title'].
def index_matrix(keywords,lines):
    indices=[]
    for j in range(len(keywords)):
        indices.append([])
    for i in range(len(lines)):
        for j in range(len(keywords)):
		if(keywords[j] in lines[i]['title']):
			indices[j].append(i)
    return indices

# Given a list "l" and a list of indices "a". The function returns a subset of 
# "l" with the indices in "a".
def subarray(l,a):
    output=[]
    for i in range(len(a)):
        output.append(l[i])
    return (output)
