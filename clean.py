import simplejson as json
def clean(t):
    output=""
    i=0
    seen=0
    while(i<len(t)):
        if(t[i]=='"'):
            if(t[i:i+8]=='"url": "'):
                output=output+ '"url": "'
                i=i+8
            elif(t[i:i+13]=='", "title": "'):
                output=output+'", "title": "'
                i=i+13
            elif(t[i:i+11]=='", "dop": "'):
                output=output+'", "dop": "'
                i=i+11
            elif(t[i:i+12]=='", "text": "'):
                output=output+'", "text": "'
                i=i+12
            elif(t[i:i+3]=='" }'):
                output=output+'" }'
                i=i+3
            else:
                i=i+1
        elif(t[i]=='\\'):
            i=i+1
        else:
            output=output+t[i]
            i=i+1
    return output

fh=open("errored.json","r")
lines=fh.readlines()
fh.close()
for i in range(len(lines)):
	lines[i]=clean(lines[i])
fh=open("cleaned.json","w")
fh.writelines(lines)
