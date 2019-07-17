from classification_function import *
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
    
    mapIndexPosition = list(zip(X, y))
    random.shuffle(mapIndexPosition)
    X, y = zip(*mapIndexPosition)
    print("shuffle done.")
    
    clf = knn(len(keywords))
    clf = clf.fit(X[:], y[:])
    print("Fitting Done")
    
    answers =  clf.predict(frequency_matrix(lines[:5],top_dict,_index_dict))
    print("Predictions Done")
    
    use = int(len(X)*0.9)
    print(len(X), use)
    correct_percent = cross_validation(clf, X[:use], y[:use], X[use:], y[use:])
    print(correct)
    
    fh=open(sys.argv[5],"w")
    for i in answers:
        fh.write(str(i))
        fh.write("\n")
    fh.close()

if __name__ == '__main__':
    '''
    There should be at max 6 inputs, 
    First the cleaned json file, 
    Second the dictionary file contaning the words,
    Third the keywords file, each separated by a line.
    Fourth the number of topwords to use
    Fifth the output file for the classification values.
    '''
    main()
