#France Paquet-Nadeau
#Feb 7

import sys
import itertools

from Recurrence_Touzet_v1 import exact_number_words  #(P,Sigma,K_dist); P is the initial word, Sigma the alphabet and K_dist the edit distance.
from Edit_Scripts_Myer_v2 import EDIT_SCRIPTS, repeating_words  #(word,d,prefix,Sigma,i,final); 'word' is the initial word, 'd' the distance, 
                                                                  #'prefix' is the starting prefix of the words we are constructing initialised as empty string, 
                                                                  #i is the iteration initialised as '0' and final is an initial empty list to store the final words. 
from Recurrences_Myer_v2 import upperbound #(k,d,s);  'k' is length of initial word, 'd' is the edit distance, 's' is size of alphabet.


def binseq(k):  #constructing all possible words of length k on a binary alphabet
    return [''.join(x) for x in itertools.product('01', repeat=k)]

K_dist=2
Sigma=['0','1']
words=binseq(4)


for w in words:
    final_list=[] #use empty list for the edit scripts
    fin=[]  #use empty list for the repeated words
    
    print(w,len(w),Sigma,'distance',K_dist)
    exact=exact_number_words(w,Sigma,K_dist)  #from Recurrence_Touzet_v1
    print('number of words in the neighbourhood',exact) #number
    
    upbound=upperbound(len(w),K_dist,len(Sigma))  #from Recurrences_Myer_v2
    
    print('upper bound for condensed neighbourhood',upbound) #number
    scripts=EDIT_SCRIPTS(w,K_dist,'',Sigma,0,final_list) #from Edit_Scripts_Myer_v2
    print('final words for condensed neighbourhood are', scripts) #list of words
    
    rep,nber=repeating_words(w,K_dist,'',Sigma,0,fin) #from Edit_Scripts_Myer_v2
    print('the repeated words in the condensed neighbourhood are',rep) #list of words and their repeats
    print('number of repetitions',nber) #number
    
    print('upperbound without repeats',upbound-nber) #number
    
    