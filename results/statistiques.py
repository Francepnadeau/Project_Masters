# France Paquet-Nadeau
# June 13, 2017
# Generating statistics based on the results files computed on Breezy.

import sys
import itertools

name = str(sys.argv[1])
with open(name) as f:
    content = f.readlines()
content = [x.strip() for x in content] 

data=[] 
for i in range(0,len(content)):
    li=content[i].split()
    data.append(filter(str.isdigit, li))
    
print(data)
