#France Paquet-Nadeau
#Jan 10, Jan 11, Jan 12, Jan 13
#Testing that the functions for the recurrences of Touzet are correct.

import networkx as nx
import sys
import itertools

K_dist=2  #maximal distance allowed between edit scripts
DULA_STATES=[] #List of binary vectors, each encoding a set of states of NULA
_X_PRIME={}

def binseq(k):  
    return [''.join(x) for x in itertools.product('01', repeat=k)]

# Creating the states of NULA(K). The states have the form (x,y) where x represents the number of errors made and y the lane.    
def states_NULA(K_dist):
    states = []  #list of possible states
    for x in range(0,K_dist+1): # x is going from 0 to K_dist for the first component of the state.
        for y in range(-x, x+1): # y is the second component of the state, goes from -x to x.
            states.append( (x,y) )    
    return(states)
    
# Insertions transitions of the automaton.
def insert(current_state, u): 
    next_state=[]    #list of possible output states          
    if current_state[0] < K_dist and u[K_dist + current_state[1]]== '0': 
        next_state.append( ( current_state[0]+1 , current_state[1]-1) )  
    return( next_state )
        
#Substitution transitions.        
def subs(current_state, u): 
    next_state=[]
    if current_state[0]<K_dist and u[K_dist + current_state[1]]== '0':   
        next_state.append( (current_state[0]+1, current_state[1]) )  
    return( next_state )
    
#Deletions followed by identity transitions.    
def delete(current_state, u):   
    next_state=[]
    for l in range(0, K_dist - current_state[0] + 1 ):  # l is an index to go from 0 to K_dist-x.
        if l == 0:  #the case where we only have identity.
            if u[K_dist + current_state[1]] == '1':  #check if the bit K_dist+y+1 in u is 1
                next_state.append( (current_state[0] , current_state[1]) )
        elif u[K_dist + current_state[1] : K_dist + current_state[1] + l + 1] == '0'*l + '1': #check if we have the correct sequence of 0's followed by '1'                                                                                    
            next_state.append( (current_state[0]+l , current_state[1]+l) )
    return( next_state )
    
#Function to perform all possible transitions of NULA(K).                
def delta(current_state, u):  # function delta_k, that tests for all the transitions from state labeled (x,y) and returns a list of the possible output states. 
                              # Input is the starting state and a bit string u, of length 2k+1.
                              # we test for all three functions and update next_state each time with the possible output
    next_state=insert(current_state, u)   # we test for the insert function
    next_state+=subs(current_state, u)    # we test for the substitution function
    next_state+=delete(current_state, u)  # we test for the delition/identity function\
    return( next_state )
    
#---------------------------------------------------------------------------------
#Testing the transitions of NULA(k).
# We run a loop on all the bit vectors of length 2k+1 and all the states of NULA(k). 
# For each state, we print the list of output states corresponding to each bit vector. We then check by hand that each of them is correct, based on the conditions
#for each type of transitions.
    
possible_state=states_NULA(K_dist)
vectors=binseq(2*K_dist+1)

for state in possible_state:
    for bit in vectors:
        if state==(0,0):
            print('from state (0,0)', bit, delta((0,0),bit))
        if state==(1,-1):
            print('from state (1,-1)', bit, delta((1,-1),bit))
        if state==(1,0):
            print('from state (1,0)', bit, delta((1,0),bit))
        if state==(1,1):
            print('from state (1,1)', bit, delta((1,1),bit))
        if state==(2,-2):
            print('from state (2,-2)', bit, delta((2,-2),bit))
        if state==(2,-1):
            print('from state (2,-1)', bit, delta((2,-1),bit))
        if state==(2,0):
            print('from state (2,0)', bit, delta((2,0),bit))
        if state==(2,1):
            print('from state (2,1)', bit, delta((2,1),bit))
        if state==(2,2):
            print('from state (2,2)', bit, delta((2,2),bit))
        
#---------------------------------------------------------------------------------

def subsumed(state1,state2):  
    if state1[0] != state2[0]: 
        if state1[0] < state2[0]: #condition on x.
            if state1[1]+state1[0]-state2[0] <= state2[1] <= state1[1]+state2[0]-state1[0]:  #conditions on y.
                return(True)
            else:
                return(False)
        elif state2[1]+state2[0]-state1[0] <= state1[1] <= state2[1]+state1[0]-state2[0]:
            return(True)
        else:
            return(False)
    else:
        return(False)
 
#--------------------------------------------------------------------------------
# Testing the subsume function.
# We run a loop over all possible distinct pairs of states in NULA(k). For each of them we test if they are not subsumed and check manually if it is correct.
# All other pairs of states are then subsumed.

for state1 in possible_state:
    for state2 in possible_state:
        if subsumed(state1,state2)== False:
            print(state1,'and',state2, 'are subsumed states')   
            
#-----------------------------------------------------------------------------------

def encod_letters(Sigma,P):  
    P_prime='$'*K_dist + P + '$'*(2*K_dist)  #We create P', which includes $'s before and after P.
    bit_vector=[]
    transition = []
    final=[None]*(len(P_prime)-2*K_dist)
    
    for i in range(len(P_prime)-2*K_dist):  #Initialising  the lists.
        final[i]=[]
        
    for letter in Sigma:  #Construct all possible bit vectors for each letter of the alphabet.
        bit = ''
        for i in range(len(P_prime)):
            if letter == P_prime[i]:  #A '1' corresponds to a match of letters.
                bit += '1'
            else:
                bit += '0'  #A '0' is any other letter.
        bit_vector.append(bit)  # We append each bit vector create by the letters.
        
    for vector in bit_vector: #Dividing every vector in substrings of length 2(K_dist)+1.
        for j in range(len(P_prime)-2*K_dist):
            if vector[j:j+2*K_dist+1] not in final[j]:
                final[j].append(vector[j:j+2*K_dist+1])
                 
    return(final)  
    
#----------------------------------------------------------------------------------
#Testing encod_letters.
#This function has a different output for different words P and alphabet Sigma. We can try different examples but ultimately we have to make sure the function is correct.
print('the encoding of the word ballad on the alphabet [a,b,d,l]',encod_letters(['a','b','l','d'],'ballad'))

#----------------------------------------------------------------------------------

def gen_state_DULA(l):  #We use l to specify which level of the tree we start on, 0 being the root level.
    global _X_PRIME

    states=states_NULA(K_dist)  #The list of states of NULA(k).
    max_dist=len(states)        #We will need to test all the states of NULA, max_dist is the number of states.
    
    if l==max_dist:
        Y=_X_PRIME.copy()  #Because appending _X_PRIME directly erases the previous entries
        DULA_STATES.append(Y)
    else:
        for i in {0,1}:
            if i==0:  #Since 0 means we do not add the state, we can always have this case.
                _X_PRIME[l]=0
                gen_state_DULA(l+1)
            else:
                for j in range(0,l): #For every state already in our list, we check if it subsumes the state we want to add.
                    if _X_PRIME[j]==1 and subsumed(states[j],states[l])==True:
                        break
                else: #If none are subsumed then we can add the state to the list.
                    _X_PRIME[l]=1
                    gen_state_DULA(l+1)
                    
gen_state_DULA(0) 

#-----------------------------------------------------------------------------------
#Testing gen_state_DULA

#Testing if every state is distinct. We run a loop on the possible states of DULA(k) and check that it does not appear later in the list.
for i in range(0,len(DULA_STATES)):
    if DULA_STATES[i] in DULA_STATES[i+1:]:
        print('Duplicate state')
    else:
        print('state',i,'is unique')
        
#Testing if every state does not contain a subsume pair of states. For every state of DULA(k), we verify that each state contained is not sumbsumed by the other states.
#We canthen check manually that all the possibilities were tested.
for state in DULA_STATES:
    for i in range(0,len(state)-1):
        for j in range(i+1,len(state)):
             if state[i]==1 and state[j]==1:
                 print(subsumed(possible_state[i],possible_state[j]),i,'and',j,'in',state,'are not subsumed')
    
        
#----------------------------------------------------------------------------------

def DULA_transition(state,bit):  
    next_state = {}  #Output state
    nula_states = states_NULA(K_dist)  #The states of NULA of the form (x,y)
    new=[]
    
    for i in range(len(state)):
        if state[i]==1:                       #We test the transition with state i of nula_states
            new += delta(nula_states[i],bit)  #Creating a list 'new' of the output states of NULA
    for j in range(len(nula_states)): #We need to reconvert these states into numbers for the states of DULA
        if nula_states[j] in new:
            next_state[j]=1
        else:
            next_state[j]=0
    return(next_state)    

#-----------------------------------------------------------------------------------
#Testing DULA_transition
# for each state of dula, find the states of nula, apply transitions, check for subsume and the check that we get the same as the the function.

#NOTE that DULA_transition does not test for subsumed states.

for state in DULA_STATES[1:]:
    for bit in vectors:
        store=[]
        new={}
        for i in range(0,len(state)):
            if state[i]==1:
                store+=(delta(possible_state[i],bit))
        for j in range(0,len(state)):
            if possible_state[j] in store:
                new[j]=1
            else:
                new[j]=0
        if new==DULA_transition(state,bit):
            print('same')
        else:
            print(state,bit, 'different')
            
#-----------------------------------------------------------------------------------
# New function for the transitions of DULA(k) that tests for subsumed states.
def new_DULA_transition(state,bit):  
    next_state = {}  #Output state
    nula_states = states_NULA(K_dist)  #The states of NULA of the form (x,y)
    new=[]
    
    for i in range(len(state)):
        if state[i]==1:                       #We test the transition with state i of nula_states
            new += delta(nula_states[i],bit)  #Creating a list 'new' of the output states of NULA
    for j in range(len(nula_states)): #We need to reconvert these states into numbers for the states of DULA
        if nula_states[j] in new:
            next_state[j]=1
        else:
            next_state[j]=0
            
    for h1 in range(0,len(state)-1):
        for h2 in range(h1,len(state)):
            if next_state[h1]==1 and next_state[h2]==1:
                if subsumed(nula_states[h1],nula_states[h2])==True:
                    next_state[h2]=0 
    if next_state in DULA_STATES:
        print('start', state, 'bit', bit, 'end', next_state)       
     
#--------------------------------------------------------------------------------
#Testing new_DULA_transition

for state in DULA_STATES[1:]:
    for bit in vectors:
        new_DULA_transition(state,bit)
                
        
        




