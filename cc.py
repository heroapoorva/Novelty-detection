import simplejson as json
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
print("Imports done")
fh=open("2014.json","r")
lines=fh.readlines()
fh.close()
#This file contains the ones which are not parseable made parseable.
fh=open("cleaned.json","r")
cleaned=fh.readlines()
fh.close()
print("Read")
#removing random symbols
def clean(t):
    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    output=REPLACE_NO_SPACE.sub("", t.lower())
    output=REPLACE_WITH_SPACE.sub(" ", t)
    return output
#Removing stopwords
english_stop_words = stopwords.words('english')
def remove_stop_words(t):
    return(' '.join([word for word in t.split() if word not in english_stop_words]))
#Lemmatization    
def get_lemmatized_text(t):
    lemmatizer = WordNetLemmatizer()
    return(' '.join([lemmatizer.lemmatize(word) for word in t.split()]))
#Running and printing in a new file
j=0
fh=open("new.json","w")
for i in range(len(lines)):
    try:
        parsed_line=(json.loads(lines[i]))
    except:
        parsed_line=(json.loads(cleaned[j]))
        j=j+1
    parsed_line["text"]=clean(parsed_line["text"])
    parsed_line["text"]=remove_stop_words(parsed_line["text"])
    parsed_line["text"]=get_lemmatized_text(parsed_line["text"])
    y=json.dumps(parsed_line)
    fh.write(y)
    fh.write("\n")
fh.close()
