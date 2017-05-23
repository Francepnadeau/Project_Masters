#France Paquet-Nadeau
#May 17, 2017
# Generating the automaton from paper of Touzet to study the size of the automaton.
#We adapted the previous code to get only the information about the automaton DULA(K).
#THE NUMBER OF TRANSITIONS RETURN DOES NOT INCLUDE THE LOOPS ON EACH STATES.

import networkx as nx
import sys
import itertools

K_start = int(sys.argv[1])
K_dist = int(sys.argv[2])
output_file=open(sys.argv[3],"w")

#Creating all bits of length 2k+1 for the transitions of DULA(k).
# Used for creating the edges of the graph for topological order.
def binseq(k):  
    return [''.join(x) for x in itertools.product('01', repeat=k)]
#-------------------------------------------------------------------------
    
# Creating the states of NULA(K). The states have the form (x,y) where x represents the number of errors made and y the lane.    
def states_NULA(K_dist):
    states = []  #list of possible states
    for x in range(0,K_dist+1): # x is going from 0 to K_dist for the first component of the state.
        for y in range(-x, x+1): # y is the second component of the state, goes from -x to x.
            states.append( (x,y) )    
    return(states)
#-------------------------------------------------------------------------
    
#Transitions of NULA(K).
#These functions take for input a state of the form (x,y) and a bit vector uof length 2k+1.
#They output a list of possible states.


# Insertions transitions of the automaton.
def insert(current_state, u,K_dist): 
    next_state=[]    #list of possible output states          
    if current_state[0] < K_dist and u[K_dist + current_state[1]]== '0': 
        next_state.append( ( current_state[0]+1 , current_state[1]-1) )  
    return( next_state )
        
#Substitution transitions.        
def subs(current_state, u,K_dist): 
    next_state=[]
    if current_state[0]<K_dist and u[K_dist + current_state[1]]== '0':   
        next_state.append( (current_state[0]+1, current_state[1]) )  
    return( next_state )
    
#Deletions followed by identity transitions.    
def delete(current_state, u,K_dist):   
    next_state=[]
    for l in range(0, K_dist - current_state[0] + 1 ):  # l is an index to go from 0 to K_dist-x.
        if l == 0:  #the case where we only have identity.
            if u[K_dist + current_state[1]] == '1':  #check if the bit K_dist+y+1 in u is 1
                next_state.append( (current_state[0] , current_state[1]) )
        elif u[K_dist + current_state[1] : K_dist + current_state[1] + l + 1] == '0'*l + '1': #check if we have the correct sequence of 0's followed by '1'                                                                                    
            next_state.append( (current_state[0]+l , current_state[1]+l) )
    return( next_state )
#------------------------------------------------------------------------------    

#Function to perform all possible transitions of NULA(K).                
def delta(current_state, u,K_dist):  # function delta_k, that tests for all the transitions from state labeled (x,y) and returns a list of the possible output states. 
                              # Input is the starting state and a bit string u, of length 2k+1.
                              # we test for all three functions and update next_state each time with the possible output
    next_state=insert(current_state, u,K_dist)   # we test for the insert function
    next_state+=subs(current_state, u,K_dist)    # we test for the substitution function
    next_state+=delete(current_state, u,K_dist)  # we test for the delition/identity function\
    return( next_state )
    
#------------------------------------------------------------------------------

#Funstion to test if two states of DULA(k) are subsumed or not. If they are, we can delete the subsumed state to reduce the number of states in DULA(k). 
# We input two states of the form (x,y) and test if either state1 subsumes state2 or state2 subsumes state1.       
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
#------------------------------------------------------------------------------
 
#Creating the states of DULA(K), based on the states and transitions of NULA(K).
#We use a recurrence tree to produce all the possible states in the form {0:0,1:0,...} where 0,1,2,...are the states of NULA(k) and for each of them, 0 means the state is not included and 1 means it is. 
#Each of {...} is a state of DULA(k) that is composed of one or more states of NULA(k).             
def gen_state_DULA(l,K_dist,X,D):  #We use l to specify which level of the tree we start on, 0 being the root level.
    global _X_PRIME
    global DULA_STATES
    
    DULA_STATES=D
    _X_PRIME=X

    states=states_NULA(K_dist)  #The list of states of NULA(k).
    max_dist=len(states)        #We will need to test all the states of NULA, max_dist is the number of states.
    
    if l==max_dist:
        Y=_X_PRIME.copy()  #Because appending _X_PRIME directly erases the previous entries
        DULA_STATES.append(Y)
    else:
        for i in [0,1]:
            if i==0:  #Since 0 means we do not add the state, we can always have this case.
                _X_PRIME[l]=0
                gen_state_DULA(l+1,K_dist,_X_PRIME,DULA_STATES)
            else:
                for j in range(0,l): #For every state already in our list, we check if it subsumes the state we want to add.
                    if _X_PRIME[j]==1 and subsumed(states[j],states[l])==True:
                        break
                else: #If none are subsumed then we can add the state to the list.
                    _X_PRIME[l]=1
                    gen_state_DULA(l+1,K_dist,_X_PRIME,DULA_STATES)
    

#-------------------------------------------------------------------------------    
    
#Creating a directed graph G for DULA(k) using our previous code and the build-in function in NetworkX

def create_graph(G,DULA_STATES,K_dist):#Creating the nodes of the graph, G is a digraph.
    list_nodes=[] # Each number i represent the state i in DULA_STATES. We do not want the first 
              # state since it is the empty state and is not part of DULA(k).
    for i in range(1,len(DULA_STATES)):
        list_nodes.append(i)
    G.add_nodes_from(list_nodes)
            
    return(G.number_of_nodes())
 
    
for k in range(K_start,K_dist+1):
    
    G=nx.DiGraph()
    gen_state_DULA(0,k,{},[])
    states=DULA_STATES
    st=create_graph(G,states,k)

    output_file.write('k='+" "+str(k)+" "+'states:'+" "+str(st)+"\n")
        
output_file.close()
