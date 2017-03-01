#France Paquet-Nadeau
#Feb 22, 2017
# Testing the recurrences of Myers by implementing a different version of these recurrences

import sys

#We assume that the stopping conditions for all the terms is k<=d or d==0. Furthermore, if d<0 in I(k,d) or D(k,d) there are no possible strings, so we return 0.

def I(k,d,s):  #We assume that I(k,d) follows the same stopping conditions as the term S(k,d)
    if k>d and d>0: #the S term followes the stoping rule k<=d or d==0
        totalSvar2=S(k-1,d,s)
        totalIvar2=s*I(k,d-1,s)
        return(totalIvar2+totalSvar2)
    elif d<0:
        return(0)
    else:
        return(1)
    
        
def D(k,d,s):
    if k>d and d>0:  #the S term followes the stoping rule k<=d or d==0
        totalSvar2=S(k-1,d,s)
        totalDvar2=D(k-1,d-1,s)
        return(totalDvar2+totalSvar2)

    elif d<0:
        return(0)
    else:
        return(1)
    
def S(k,d,s): #the recurrences are the same
    if k<=d or d==0:
        return(1)
    else:
        total=S(k-1,d,s)+(s-1)*S(k-1,d-1,s)+(s-1)*I(k-1,d-1,s)+pow(s-1,2)*I(k-1,d-2,s)+D(k-1,d-1,s)
        return(total) 
        
def sum_first_ins(k,d,s): #insertions before the first symbol of the word.
    total=0
    for j in range(1,d+1):
        total+=pow(s,j)*S(k-1,d-j,s)
    return(total)  
    
def upperbound_check(k,d,s):
    total=S(k,d,s)+sum_first_ins(k,d,s)
    return(total)    