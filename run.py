from novelty_function import *
def main():
    
    input_file = open(sys.argv[1], "r")
    lines = input_file.readlines()
    
    dict_file = open(sys.argv[2], "r")
    data = json.load(dict_file)
    
    (top_dict,indices)=get_top(int(sys.argv[3]),data)
    print("got dictionary")
    
    lines=dictionary_array(lines)
    print("Parsing finished!")

    (start_position,end_position)=date_dictionary(lines)
    print("Dictionary created")
    
    values = sliding_window_tfidf(lines,top_dict,indices,int(sys.argv[4]))
    
    fh=open(sys.argv[5], "w")
    for i in values:
        fh.write(str(i))
        fh.write(" ")
    fh.close()
    input_file.close()
    dict_file.close()
    
if __name__ == '__main__':
    '''
    There should be at max 5 inputs, 
    First the cleaned json file, 
    Second the dictionary file contaning the words,
    Third the number of topwords to use
    Fourth the window size 
    Lastly the output file for the novelty values.
    '''
    main()
