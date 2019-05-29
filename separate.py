#importing libraries
#SimpleJSON is better for loading this up
import simplejson as json
import numpy as np
#Creating the json objects for each
fh=open("2014.json","r")
lines=fh.readlines()
fh.close()
output=[]
for i in range(len(lines)):
    try:
        json.loads(lines[i])
    except:
        output.append(lines[i])
fh=open("errored.json","w")
fh.writelines(output)
