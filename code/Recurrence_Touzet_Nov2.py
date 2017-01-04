#France Paquet-Nadeau
#November 2, 2016
#Implementation of the recurrence relations found in "On the Levenshtein Automaton and the Size of the Neighbourhood of a word" 
# by Helene Touzet.

import networkx as nx
import sys
import itertools

K_dist=1
DULA_STATES=[] #List of binary vectors, each encoding a set of states of NULA
_X_PRIME={}

def binseq(k):  #creating all bits of length 2k+1 for the transitions of DULA(k)
    return [''.join(x) for x in itertools.product('01', repeat=k)]
    
def states_NULA(K_dist):
    states = []  #possible states
    for i in range(0,K_dist+1): 
        x = i
        for j in range(-x, x+1):  
            y = j
            states.append( (x,y) )    
    return(states)
#transitions of NULA

def insert(current_state, u): #uses as input a state and a bit string u
    next_state=[]
    if current_state[0] < K_dist and u[K_dist + current_state[1]]== '0':  
        next_state.append( ( current_state[0]+1 , current_state[1]-1) )  
    return( next_state )
        
def subs(current_state, u):   # substitution transition
    next_state=[]
    if current_state[0]<K_dist and u[K_dist + current_state[1]]== '0':   
        next_state.append( (current_state[0]+1, current_state[1]) )  
    return( next_state )
    
def delete(current_state, u):   #deletion + identity transition
    next_state=[]
    for i in range(0, K_dist - current_state[0] + 1 ):  
        l = i
        if l == 0:
            if u[K_dist + current_state[1]] == '1':  #check if the bit k+y+1 in u is 1
                next_state.append( (current_state[0] , current_state[1]) )
        elif u[K_dist + current_state[1] : K_dist + current_state[1] + l + 1] == '0'*l + '1': 
                                                                                               
            next_state.append( (current_state[0]+l , current_state[1]+l) )
    return( next_state )
        
def delta(current_state, u):  # function delta_k, that tests for all the transitions from state labeled u and returns a list of the possible output states. 
                              # Input is the starting state and a bit string u, of length 2k+1.
                              # we test for all three functions and update next_state each time with the possible output
    next_state=insert(current_state, u)   # we test for the insert function
    next_state+=subs(current_state, u)    # we test for the substitution function
    next_state+=delete(current_state, u)  # we test for the delition/identity function\
    return( next_state )
def subsumed(state1,state2):  #states are of the form (x,y)
    if state1[0] != state2[0]:
        if state1[0] < state2[0]:
            if state1[1]+state1[0]-state2[0] <= state2[1] <= state1[1]+state2[0]-state1[0]:
                return(True)
            else:
                return(False)
        elif state2[1]+state2[0]-state1[0] <= state1[1] <= state2[1]+state1[0]-state2[0]:
            return(True)
        else:
            return(False)
    else:
        return(False)
def gen_state_DULA(l):
    global _X_PRIME

    states=states_NULA(K_dist)  #The list of states of NULA(k)
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
                else: #If none are subsume then we can add the state to the list.
                    _X_PRIME[l]=1
                    gen_state_DULA(l+1)
                    
gen_state_DULA(0)

#--------------------------------------------------------------------------
#Function alpha that counts the number of possible letter associate to a bit vector of a word P.
#u is a bit vector of length 2k+1, P is our word , Sigma is the alphabet and i is the substring we want to consider.

def alpha(u,i,P,Sigma):
    if '1' in u:
        return(1)
    else:
        P_prime='$'*K_dist+P+'$'*(2*K_dist)
        P_op=P_prime[i-1:i+2*K_dist]  #take the substring of P
        p_list=[]
        for letter in P_op: #Convert the substring of P to a list containing its letters
            p_list.append(letter)
        p_set=set(p_list) #Convert to a set to get rid of duplicate letters
        if '$' in p_set:
            p_set.remove('$')
        value=len(Sigma)-len(p_set)
        return(value)
        
#We generate only the transitions for the states {0,..m+k} of Encod(P,k) as we do not need those of the $ states to compute the 
# recurrence relations.

def encod_letters(Sigma,P):  #sigma is a list of letters, P is the original word
    P_prime='$'*K_dist + P + '$'*(2*K_dist)  #We want to have bit vectors representing only the $'s at the end, not at the front
    bit_vector=[]
    transition = []
    final=[None]*(len(P_prime)-2*K_dist)
    for i in range(len(P_prime)-2*K_dist):
        final[i]=[]
        
    for letter in Sigma:  #Construct all possible bit vectors for each letter of the alphabet
        bit = ''
        for i in range(len(P_prime)):
            if letter == P_prime[i]:
                bit += '1'
            else:
                bit += '0'
        bit_vector.append(bit)
        
    for vector in bit_vector: #Divide every vector in substring of length 2(K_dist)+1
        for j in range(len(P_prime)-2*K_dist):
            vec=''
            for i in range(j,j+2*K_dist+1):
                vec+=vector[i]
            transition.append(((vec),j)) 
        
    for j in range(len(P_prime)-2*K_dist): #Sort the elements of transition by order and eleminate duplicate
        for i in range(len(transition)):
            if transition[i][1]==j and transition[i][0] not in final[j]:
                final[j].append(transition[i][0])
    
    return(final)
def DULA_transition(state,bit):  #Using a state of DULA of the form {0:0, 1:1,..} and a bit vector of the form '001'
    next_state = {}
    nula_states = states_NULA(K_dist)  #The states of NULA of the form (x,y)
    new=[]
    
    for i in range(len(state)):
        if state[i]==1:                       #We test the transition with state i of nula_states
            new += delta(nula_states[i],bit)   #Creating a list 'new' of the output states of NULA
    for j in range(len(nula_states)): #We need to reconvert these states into numbers for the states of DULA
        if nula_states[j] in new:
            next_state[j]=1
        else:
            next_state[j]=0
    return(next_state)
    
#creating a directed graph G of DULA(k) using our previous code and the build-in function in NetworkX
G=nx.DiGraph()

#Creating the nodes of the graph
list_nodes=[] #we create a list of nodes for the graph. Each number i represent the state i in DULA_STATES. We do not want the first 
              # state since it is the empty state and is not part of DULA(k).
for i in range(1,len(DULA_STATES)):
    list_nodes.append(i)

G.add_nodes_from(list_nodes)

#Creating the edges of the graph
possible_bits=binseq(2*K_dist+1)  #need all possible bit vectors of length 2k+1 for the transitions

for state in DULA_STATES[1:]:
    for bit in possible_bits:
        next_state=DULA_transition(state,bit)
        if next_state != DULA_STATES[0] and next_state in DULA_STATES:  #need to ensure that the next state is part of our possible states.
            new=DULA_STATES.index(next_state)
            current=DULA_STATES.index(state)
            if current != new:  #we need to delete the loops on every state, otherwise topological_sort sees a cycle
                G.add_edge(current,new)
              
              
#topological sort of the states of DULA(k) 
order=nx.topological_sort(G)

#order is a list of numbers, each of them represents the position of the state in DULA_STATES

#change it back to a list of states
DULA_order=[]
for i in range(0,len(order)):
    DULA_order.append(DULA_STATES[order[i]])

#0,1,2,3 are the states of NULA: 0-(0,0), 1-(1,-1), 2-(1,0), 3-(1,1) when k=1
#For each state, 0:0 means the state 0 is not in and 0:1 means the state 0 is in the set of states.
# Implementation of the recurrences using a table

def S(P,Sigma):
    #initialising the table
    m=len(P)
    I_order=[]  #list of states of Encod(P,k). There are m+k states + 2k $-states
    for i in range(0,m+3*K_dist+1):
        I_order.append(i)
    UNASSIGNED=0

    S_TABLE={}
    for q in range(0,len(DULA_order)-1): # We do not want the last stateas as it is not part of DULA
        S_TABLE[q]={}
        for i in I_order:
            S_TABLE[q][i]=UNASSIGNED
    S_TABLE[0][0]=1
    
    
    times=1 #will be used to count the number of 1's in the bit vector u for states $
    for i in I_order:
        j=i
    #---------------------------------------------------------------------------------------------------------------------------------
    # recurrences for states {0,..,m+k} of Encod(P,k)
        if j>=1 and j<=m+K_dist:
            for q in range(0,len(DULA_order)-1):  #q is the number of the row, corresponding to the state in DULA_order.                                   
                tab=0
                bit_vectors=encod_letters(Sigma,P)[i-1]   
                print("DEBUG ---->"+str(bit_vectors))
                for u in bit_vectors:
                    print("DEBUG "+str(u))
                    al=alpha(u,i,P,Sigma)
                    count=0
                    for state in DULA_order[0:q+1]:
                        if DULA_order[q] == DULA_transition(state,u):
                            tab+=al*S_TABLE[count][i-1]
                            count+=1
                        else:
                            count+=1
                S_TABLE[q][i]=tab
    
    #----------------------------------------------------------------------------------------
    # recurrences for the first $ state
    
        if j==m+K_dist+1:
            for q in range(0,len(DULA_order)-1):
                count1=0
                tab1=0
                for state in DULA_order[0:q+1]:
                    #u='001'
                    if DULA_order[q] == DULA_transition(state,'0'*(2*K_dist)+'1'):
                        tab1+= S_TABLE[count1][j-2*K_dist-1]
                        count1+=1
                    else:
                        count1+=1
                S_TABLE[q][j]=tab1
                        
    #----------------------------------------------------------------------------------------
    # recurrences for the other $ states
    #need to make general case for bit vector u
    
        if j>m+K_dist+1:
            times+=1 #keep track of the number of 1's in the bit vector u for transition to state j
            for q in range(0,len(DULA_order)-1):
                count2=0
                tab2=0
                for state in DULA_order[0:q+1]:
                    if DULA_order[q]== DULA_transition(state,'0'*(2*K_dist+1-times)+'1'*times):
                        tab2+=S_TABLE[count2][j-2*K_dist-1]+S_TABLE[count2][j-1] 
                        count2+=1
                    else:
                        count2+=1 
                S_TABLE[q][j]=tab2
        
    return(S_TABLE)
             
             
            
# before using a table cell (p,u) write "assert (S[p][u]!=UNASSIGNED), print("Error: accessing unassigned cell "+str((p,u))+" while computing "+str((q,i))"
 
def S_TOTAL(P,Sigma):
    S_table=S(P,Sigma)
    total=0
    m=len(P)
    for q in range(0,len(DULA_order)-1):
        total+=S_table[q][m+K_dist]+S_table[q][m+3*K_dist]
    return(total)
               

TAB=S(sys.argv[1],['a','b','l'])
print("TABLE "+str(TAB))
for i in TAB.keys():
    TABi=TAB[i]
    for j in TABi.keys():
        if TABi[j]>0:
            print(str(i)+","+str(j)+":"+str(TABi[j]))
RES=S_TOTAL(sys.argv[1],['a','b','l'])
print("RESULT "+str(RES))
