#France Paquet-Nadeau
#Oct 1 - oct 3
#Generating the edit scripts using the recurrences in Gene Myer's paper 'What's behind BLAST?', p.10.
#These recurrences are an upper bound for the number of edit scripts in the condensed neighborhood of a word with d differences on an alphabet Sigma.

#We break down the recurrences to have a procedure for each term.

#We will break down the initial word by increasing the prefix for each opperation we do. For each of the procedures, we will increase
# the length of the prefix, depending on wich operation we are doing.

import sys

#The first letter of word is a match. We increment prefix with that letter and reduce word by one letter.
def EDIT_SCRIPTS_match(word,d,prefix): 
    prefix+=word[0]
    return(word[1:],d,prefix)
    
#the first letter of word will be a substitution
#We do not allow to substitute for the same letter
def EDIT_SCRIPTS_sub(word,d,prefix,Sigma):
    list1=[]    #will be used to store the different words obtain by doing the substitutions
    for letter in Sigma:
        new_pref=''.join(prefix)
        if letter != word[0]:
            new_pref+=letter
            list1.append((word[1:],d-1,new_pref))
    return(list1)
    
# Sequence of insertions after a letter, we insert between the first and second letters of word
# Each sequence of insert finishes with a match of second letter of word
def EDIT_SCRIPTS_ins(word,d,prefix,Sigma,i,list4):  #we use i to know if we are starting a new sequence of insertions or if we are adding to the sequence     
    k=len(word)
    if k<=d or d==0:
        return
    else:
        if i == 0:  #the first insert in the sequence, we do not allow it to be the same as the previous letter in word.
            for letter in Sigma:
                new_pref=''.join(prefix)
                if letter != word[0]:
                    new_pref+=word[0]+letter
                    list4.append((word[2:],d-1,new_pref+word[1]))  #for each possible letter, we save it in list4
                    EDIT_SCRIPTS_ins(word[1:],d-1,new_pref,Sigma,1,list4)
        else:
            for letter in Sigma:  #continuing the insertion sequence
                new_pref=''.join(prefix)
                new_pref+=letter
                list4.append((word[1:],d-1,new_pref+word[0]))
                EDIT_SCRIPTS_ins(word,d-1,new_pref,Sigma,1,list4)
        return(list4)
        
#sequence of deletions
#Each sequence of deletion finishes with a match on the following letter(the first non-deleted one)
def EDIT_SCRIPTS_del(word,d,prefix,Sigma,list5): 
    k=len(word)
    if k<=d or d==0:
        return
    else:
        prefix+='-'
        list5.append((word[2:],d-1,prefix+word[1]))
        EDIT_SCRIPTS_del(word[1:],d-1,prefix,Sigma,list5)
        return(list5)
        
# substitution + sequence of at least one insertions. We substitute the first letter and start a sequence of insertions.
#The sequence will finish with a match
def EDIT_SCRIPTS_subins(word,d,prefix,Sigma,i,list2):  #We use i as an index to know if we are starting a new sequence
    k=len(word)
    if k<=d or d==0:
        return
    else:
        if i == 0 and d>=2:  
            for letter in Sigma:  #substitution
                new_pref=''.join(prefix)
                if letter != word[0]:
                    new_pref+=letter
                    for letter in Sigma:  #first insertion
                        if letter != new_pref:
                            new_pref2=''.join(new_pref)
                            new_pref2+=letter
                            list2.append((word[2:],d-2,new_pref2+word[1]))
                            EDIT_SCRIPTS_subins(word[1:],d-2,new_pref2,Sigma,1,list2)
                            
        elif i == 1:
            for letter in Sigma:
                new_pref=''.join(prefix)
                new_pref+=letter
                list2.append((word[1:],d-1,new_pref+word[0]))
                EDIT_SCRIPTS_subins(word,d-1,new_pref,Sigma,1,list2)   
    return(list2)    
    
#Insertion before the first letter of the word. There are no restrictions on the possible inserts
#ONLY DO ONCE
def first_ins(word,d,prefix,Sigma,list1):
    k=len(word)
    if k<=d or d==0:
        return
    else:
        for letter in Sigma:
            new_pref=''.join(prefix)
            new_pref+=letter
            list1.append((word[1:],d-1,new_pref+word[0]))
            first_ins(word,d-1,new_pref,Sigma,list1)
    return(list1)
    
# putting everything together
#This will generate the possible edit scripts
final_words=[]
def EDIT_SCRIPTS_FINAL(word,d,prefix,Sigma,i):
    global transit,final_words
    k=len(word)
    
    if i==0:
        transit=first_ins(word,d,prefix,Sigma,[])  #initializinf the list of unfinished words with the insertion before the first letter
    
    if k<=d or d==0:  #stopping condition, rebuild the edit script by putting the prefix with the rest of the word
        final_words.append(prefix+word)  
        return
    else:
        #calling the possible edits
        transit.append(EDIT_SCRIPTS_match(word,d,prefix))
        transit2=(EDIT_SCRIPTS_sub(word,d,prefix,Sigma))
        transit.extend(transit2)  #We want to append the elements, not the list
        transit2=(EDIT_SCRIPTS_ins(word,d,prefix,Sigma,0,[]))
        transit.extend(transit2)
        transit2=(EDIT_SCRIPTS_del(word,d,prefix,Sigma,[]))
        transit.extend(transit2)
        transit2=(EDIT_SCRIPTS_subins(word,d,prefix,Sigma,0,[]))
        transit.extend(transit2)

        while transit != []:
            word,d,prefix=transit.pop()
            EDIT_SCRIPTS_FINAL(word,d,prefix,Sigma,1)  
            
                           
alphabet=['a','b']
words=['abbaa','babbaa','bbabba','abbbbab','ababa','aababa']
final_words=[]
for i in range(0,6):
    EDIT_SCRIPTS_FINAL(words[i],2,'',alphabet,0)
    for i in range(0,len(final_words)):
        if '-' in final_words[i]:
            final_words[i]=final_words[i].replace('-','')
    
    print(len(final_words))
    final_words=[]
    
#counting the number of repeating words in the list that generates the words int the condensed neighborhood

final_words=[]
EDIT_SCRIPTS_FINAL('aabab',2,'',['a','b'],0)
for i in range(0,len(final_words)):
        if '-' in final_words[i]:
            final_words[i]=final_words[i].replace('-','')
#print(len(final_words))

repeats=[]
for i in range(0,len(final_words)-1):
    k=1
    if final_words[i] not in repeats:
        w=final_words[i]
        for j in range(i+1,len(final_words)):
            if w==final_words[j]:
                k+=1
        if k !=1:
            repeats.append(w)
            repeats.append(k)
                
print(repeats)               
