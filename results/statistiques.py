# France Paquet-Nadeau
# June 13, 2017
# Generating statistics based on the results files computed on Breezy.

import sys
import itertools


f = open("5_1_results","r")  #state the name of the file to import
fdata=[]

for line in f.readfiles():
    fdata.append([])
    fdata[i].append(line)

d=[]  #storing the relevant data from the file
for line in range(len(f.readlines())-2):
    d.append([])
    
print(d)