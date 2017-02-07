# France Paquet-Nadeau
# Jan25 2017
# Recurrences in Gene Myer article 'What's behind BLAST' p.10
# We use the parameters 'k' for the length of the word, 'd' for the edit distance and 's' for the length of the alphabet.

import sys

def sum1(k,d,s):  #summation for inserts 
    total=0
    for j in range(0,d):
        total+=pow(s,j)*S(k-2,d-1-j,s)
    return(total)

def sum2(k,d,s):  #summation for substitution followed by insertions
    total=0
    for j in range(0,d-1):
        total+=pow(s,j)*S(k-2,d-2-j,s)
    return(total)

def sum3(k,d,s):  #summation for deletion
    total=0
    for j in range(0,d):
        total+=S(k-2-j,d-1-j,s)
    return(total)


def S(k,d,s):  #combining everything together
    if k<=d or d==0:
        return(1)
    else:
        total=S(k-1,d,s)+(s-1)*S(k-1,d-1,s)+(s-1)*sum1(k,d,s)+pow(s-1,2)*sum2(k,d,s)+sum3(k,d,s)
        return(total)


def sum4(k,d,s): #insertions before the first symbol of the word.
    total=0
    for j in range(1,d+1):
        total+=pow(s,j)*S(k-1,d-j,s)
    return(total)

#upper bound for the condensed d-neighborhood of a word

def upperbound(k,d,s):
    total=S(k,d,s)+sum4(k,d,s)
    return(total)
 