from dictionary_function import *

def main():
    f=open(sys.argv[1],'r')
    d={}
    # this will contain all words in a given file
    # We will print these out in another file
    for i, line in enumerate(f):
        temp_json=json.loads(line)
        temp_text=temp_json["text"].split()
        for word in temp_text:
            if(word in d):
                d[word]=d[word]+1
            else:
                d[word]=1
    f.close()
    with open(sys.argv[2], 'w') as outfile:  
        json.dump(d, outfile)

if __name__ == '__main__':
    '''
    There should be at max 2 inputs, the first the cleaned json file, second 
    the output file for the dictionary to be wirtten.
    '''
    main()
