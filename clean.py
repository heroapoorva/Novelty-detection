from cleaning_function import *
def main():
    read_file = open(sys.argv[1], "r")
    while(True):
        '''
        For a given news file, we read as many lines as many cores are there
        for use, each of these core will clean a separate news article.
        Cleaning includes, making the news article json parseable, removing 
        special characters, removing stopwords and finally lemmatizing.
        '''
        lines = []
        for i in range(mp.cpu_count()):
            lines.append(read_file.readline())
        pool = mp.Pool(processes = mp.cpu_count())
        news=[]
        news=pool.map(final_function, (lines[i] for i in range(len(lines)) ))
        write_file=open(sys.argv[2],"w")
        for new in news:
            if(new != ""):
                write_file.write(new)
                write_file.write("\n")
        if("" in news):
            break
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
