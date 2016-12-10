# France Paquet-Nadeau
# November 9, 2016
# Recurrences in Gene Myer article 'What's behind BLAST' p.10
#This is the implementation of the recurrences relation presented in the paper.

import sys

#We use: k to represent the length of the query/ the length of the word,
# d is the number of differences allowed
# s is the size of the alphabet.

def sum1(k,d,s):  #summation for inserts, counting the terms associated with a sequence of insertions 
    total=0
    for j in range(0,d):
        total+=pow(s,j)*S(k-2,d-1-j,s)
    return(total)

def sum2(k,d,s):  #summation for sub+ins, counting the terms that start with a substitution followed by a sequence of insertions
    total=0
    for j in range(0,d-1):
        total+=pow(s,j)*S(k-2,d-2-j,s)
    return(total)

def sum3(k,d,s):  #summation for deletion, counting a sequence of deletions
    total=0
    for j in range(0,d):
        total+=pow(s,j)*S(k-2-j,d-1-j,s)
    return(total)


def S(k,d,s): # Summing all the terms together
    if k<=d or d==0:
        return(1)
    else:
        return(S(k-1,d,s)+(s-1)*S(k-1,d-1,s)+(s-1)*sum1(k,d,s)+pow(s-1,2)*sum2(k,d,s)+sum3(k,d,s))


def sum4(k,d,s): # Adding the case where the insertions happen before the first symbol of the query.
    total=0
    for j in range(1,d+1):
        total+=pow(s,j)*S(k-1,d-j,s)
    return(total)

#----------------------------------------------------------
# For the final upperbound
def upperbound(k,d,s):
    return(S(k,d,s)+sum4(k,d,s))

