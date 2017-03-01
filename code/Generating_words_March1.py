#France Paquet-Nadeau
# Generating the words from the recurrences of Gene Myers
# Feb 21
#We start with an empty list that will be used to keep track of the remaining letters in the initial word, the remaining distance and the prefix we are constructing.

import sys

global constructing_list_of_final_words  #we use this list to store the remaining letters in 'word', the new distance and prefix. 
                                         #Each function adds elements to this list.

#match function
def Word_match(word,d,prefix): #we match the first letter left in 'word', we add it to the prefix and theen delete it from 'word'.
    prefix+=word[0]            #corresponds to S(k-1,d)
    constructing_list_of_final_words.append((word[1:],d,prefix)) 
    
#Substitution function
def Word_sub(word,d,prefix,Sigma): #substitution function, we substitute the first letter of 'word' and add it to 'prefix'
    for letter in Sigma:           #corresponds to S(k-1,d-1)
        new_pref=''.join(prefix)
        if letter != word[0]:  #we can substitute for any other letter of the alphabet
            new_pref+=letter
            constructing_list_of_final_words.append((word[1:],d-1,new_pref)) 
       
#insertion function
def Word_ins(word,d,prefix,Sigma,j):  #we use j to know if we are starting a new sequence of insertions or if we are adding to the sequence 
                                      #We do insertions after a character   
    k=len(word)
    if k<=d or d==0:
        return 
    elif j==0 and d>=1 and k>=2:
        for letter in Sigma:  #the first insertion cannot be the same letter as the preceding one in 'word'
                new_pref=''.join(prefix)
                if letter != word[0]:  #we can insert any of the other letters in the alphabet
                    new_pref+=word[0]+letter
                    constructing_list_of_final_words.append((word[2:],d-1,new_pref+word[1]))  #corresponds to (s-1)S(k-2,d-1)
                    Word_ins(word[1:],d-1,new_pref,Sigma,1)
    elif d>=0:
        for letter in Sigma:  #continuing the insertion sequence by calling the function again until we have reached d=0
            new_pref=''.join(prefix)
            new_pref+=letter
            constructing_list_of_final_words.append((word[1:],d-1,new_pref+word[0]))  #corresponds to (s-1)S(k-2,d-1-j) for j between 1 and d-1
            Word_ins(word,d-1,new_pref,Sigma,1)
    
#deletion function
def Word_del(word,d,prefix,Sigma):
    j=0 #index for the number of deletion done so far
    k=len(word)
    while j <=d-1:
        if k<=d or d==0: #or len(word)<2+j:
            return
        else:
            constructing_list_of_final_words.append((word[2+j:],d-1-j,prefix+word[1+j])) #corresponds to S(k-2-j,d-1-j)
            j+=1
           
#substitution followed by insertion
def Word_subins(word,d,prefix,Sigma,i):  #We use i as an index to know if we are starting a new sequence of insertion after a substitution
                                         #We use i=0 to signify that we are starting a substitution and a sequence of insertions. 
                                         #When i=1, we have done a substitution and the first insertion in the sequence.
    k=len(word)
    if k<=d or d==0:
        return
    else:
        if i == 0: 
            if d>=2 and k>=2: 
                for letter in Sigma:  #substitution
                    new_pref=''.join(prefix)
                    if letter != word[0]:
                        new_pref+=letter
                        for letter in Sigma:  #first insertion
                            if letter != new_pref[-1]:
                                new_pref2=''.join(new_pref)
                                new_pref2+=letter
                                constructing_list_of_final_words.append((word[2:],d-2,new_pref2+word[1]))
                                Word_subins(word[1:],d-2,new_pref2,Sigma,1)
            else:
                return
        elif i==1:  
            if d>=0:  #consitinuig the sequence of insertion
                for letter in Sigma:
                    new_pref=''.join(prefix)
                    new_pref+=letter
                    constructing_list_of_final_words.append((word[1:],d-1,new_pref+word[0]))
                    Word_subins(word,d-1,new_pref,Sigma,1)
            else:
                return
    
# insertion before the fisrt character
def Word_first_ins(word,d,prefix,Sigma):
    k=len(word)
    if k<=d or d==0:
        return
    else:
        for letter in Sigma:  #there is no restriction on the letters
            new_pref=''.join(prefix)
            new_pref+=letter
            constructing_list_of_final_words.append((word[1:],d-1,new_pref+word[0]))
            Word_first_ins(word,d-1,new_pref,Sigma)

#Recurrences
final_words=[]
def Generating_words(word,d,prefix,Sigma,initial_list):
    global constructing_list_of_final_words
    
    constructing_list_of_final_words=initial_list
    count=0  #We will use this index to count the number of words generated
    constructing_list_of_final_words.append((word,d,''))
    Word_first_ins(word,d,prefix,Sigma) # appends the original list with the first strings
    
    while constructing_list_of_final_words != []:
        word,d,pref=constructing_list_of_final_words.pop()
        if len(word)<=d or d==0: #stopping condition
            count+=1
            final_words.append(pref+word)
        else:        #for every element in the list, we perform the possible operations
            Word_match(word,d,pref)
            Word_sub(word,d,pref,Sigma)
            Word_ins(word,d,pref,Sigma,0)
            Word_del(word,d,pref,Sigma)
            Word_subins(word,d,pref,Sigma,0)
    return(count) #We return only the total number of words generated, the words themselves are in the list 'final_words'.
 
