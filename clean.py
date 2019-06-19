from functions import *

fh=open("2014.json","r")
lines=fh.readlines()
fh.close()
pool = mp.Pool(processes=mp.cpu_count())
print("starting to make new.")
new=pool.map(final_function, (lines[i] for i in range(len(lines)) ))
print("finished making new.")
fh=open("clean.json","w")
for i in range(len(lines)):
    fh.write(new[i])
    fh.write("\n")
fh.close()
