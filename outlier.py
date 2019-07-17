from outlier_function import *
def main():
    with open(sys.argv[1]) as json_file:  
        lines=json_file.readlines()
    with open(sys.argv[2]) as json_file:  
        data = json.load(json_file)
    with open(sys.argv[3]) as read_file:  
        temp_keywords = read_file.readlines()
    print("Read the news files and the dictionary")
    
    keywords=[]
    for temp_keyword in temp_keywords:
        keywords.append((temp_keyword.lower())[:-1])
    '''
    pool = mp.Pool(processes=mp.cpu_count())
    keywords=pool.map(remove_junk, (keywords[j] for j in range(len(keywords)) ))
    keywords=pool.map(remove_stop_words,(keywords[j] for j in range(len(keywords)) ))
    keywords=pool.map(get_lemmatized_text,(keywords[j] for j in range(len(keywords)) ))
    '''
    print("Names are cleared")
    
    (top_dict,index_dict)=get_top(int(sys.argv[4]),data)
    print("got dictionary")
    
    lines=dictionary_array(lines)
    print("Parsing finished!")
    
    indices=index_matrix(keywords,lines)
    
    fh=open(sys.argv[6],"w")
    for i in range(len(indices)):
        matrix=subarray(lines,indices[i])
        values=sliding_window_tfidf(matrix,top_dict,index_dict,int(sys.argv[5]))
        for j in values:
            fh.write(str(j))
            fh.write(" ")
        fh.write("\n")
    fh.close()
    
if __name__ == '__main__':
    '''
    There should be at max 6 inputs, 
    First the cleaned json file, 
    Second the dictionary file contaning the words,
    Third the keywords file, each separated by a line.
    Fourth the number of topwords to use
    Fifth the window size 
    Lastly the output file for the novelty values.
    '''
    main()
