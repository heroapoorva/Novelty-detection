from functions import *
# declare empty dictionary
d={}
# this will contain all words in a given file
# We will print these out in another file
filename='clean.json'
f=open(filename,'r')
i=0
for x in f:
    temp_json=json.loads(x)
    temp_text=temp_json["text"].split()
    for word in temp_text:
        if(word in d):
            d[word]=d[word]+1
        else:
            d[word]=1
f.close()
with open('dict.json', 'w') as outfile:  
    json.dump(d, outfile)
