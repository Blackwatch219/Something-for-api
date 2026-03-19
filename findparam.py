
import json
import re
import requests
import sys
import os

fileurl=sys.argv[1]

filemkdir=fileurl.split('_')[0]
if not os.path.exists(filemkdir):
    os.makedirs(filemkdir)


#get path  + 路径名称
paths=[]
for dirpath, dirnames, filenames in os.walk('./'+filemkdir):
    for file in filenames:
        with open("./"+filemkdir+"/"+file,"r",encoding='gb18030', errors='ignore') as f2:
            try:
                line=f2.readlines()
                for line in line:
                    line=line.strip('\n').strip('\t')
                    #print(line)
                    p = re.findall(r'[a-zA-Z]+[\w-]*\d*|\d+[\w-]*[a-zA-Z]+|[a-zA-Z]+\.[a-zA-Z]+|\w+\.\d+|[a-zA-Z]+~[a-zA-Z]+|\w+~\d+|\d+-\d+|[a-zA-Z]+-[a-zA-Z]+', line)
                    #print(p)
                    if p != None:
                        #print(p)
                        for path in p:
                            path=path.replace(':"',"").replace('"',"")
                            paths.append(path)
            except Exception as e:
                print(e)


for var in sorted(set(paths)):
    with open (fileurl+'_param.txt',"a+",encoding='gb18030', errors='ignore') as paths:
        paths.write(var+'\n')
