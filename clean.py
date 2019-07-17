from cleaning_function import *
def main():
    read_file = open(sys.argv[1], "r")
    write_file=open(sys.argv[2],"w")
    '''
    For a given news file, we read as many lines as many cores are there
    for use, each of these core will clean a separate news article.
    Cleaning includes, making the news article json parseable, removing 
    special characters, removing stopwords and finally lemmatizing.
    '''
    lines = []
    for i, line in enumerate(read_file):
        line = final_function(line)
        if(line != ''):
            write_file.write(line)
            write_file.write("\n")
    read_file.close()
    write_file.close()
    
if __name__ == '__main__':
    '''
    There should be atmax 2 arguements given to this function 
    the first being the relative path to the news data which is to be cleaned, 
    the second being the output file where the cleaned news data is to be 
    written.
    Just make sure there are no empty lines in the middle.
    '''
    main()
