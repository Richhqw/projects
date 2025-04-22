from tkinter import filedialog, messagebox
import re
file= filedialog.askopenfilename()
fp= open(file,"r")
no_input= int(fp.readline())
inputs=[]
#gets the text inputs
for i in range(no_input):
    temp_input= fp.readline().strip()
    inputs.append(temp_input)

#Get the states
states= fp.readline().strip()
states = re.split(" ",states)
#Get the observable states
obs_states= fp.readline().strip()
obs_states=re.split(" ",obs_states)
obs_prob=[]
"""
    Calculates the Value of State sub n
    Calls itself until it reaches the base case which is n=0 and return its corresponding value in the base_val
"""
def calculate_i(base_val, given_prob, find):
    if find[1]==0:
        # print("Base Cased Reached")
        return base_val[find[0]]
    else:
        
        temp_sum = (given_prob[0][find[0]] *calculate_i(base_val,given_prob,(0,find[1]-1))) +(given_prob[1][find[0]] *calculate_i(base_val,given_prob,(1,find[1]-1)))+(given_prob[2][find[0]] *calculate_i(base_val,given_prob,(2,find[1]-1))) + (given_prob[3][find[0]] *calculate_i(base_val,given_prob,(3,find[1]-1)))
        return temp_sum    

# Calculates the Observable State sub n
def calculate_o(base_val, given_prob, find,obs_prob):

    temp_sum = (obs_prob[0][find[0]] *calculate_i(base_val,given_prob,(0,find[1]))) +(obs_prob[1][find[0]] *calculate_i(base_val,given_prob,(1,find[1])))+(obs_prob[2][find[0]] *calculate_i(base_val,given_prob,(2,find[1])))+(obs_prob[3][find[0]] *calculate_i(base_val,given_prob,(3,find[1])))
    return temp_sum    
        
for i in range(len(states)):
    temp = fp.readline().strip()
    temp=re.split(" ", temp)
    temp = [float(element) for element  in temp]
    obs_prob.append(temp)
no_solve= int(fp.readline())
to_solve_list=[] #solve 
to_solve_list_string=[] #string version
for j in range(no_solve):
    solve= fp.readline().strip()
    to_solve_list_string.append(solve)
    solve= "".join(solve.split("given")) # REmoves given
    solve= solve.split(" ")
    
    solve.pop(1)
    to_solve_list.append(solve)
fp.close
fp = open("output.out","w")

for i in range(no_input):
    print(f"Solving : {inputs[i]}")
    fp.write(f"Solving : {inputs[i]}\n\n")
    given_prob=[]
    #Setup the array for given values
    given_total=[]
    for j in range(len(states)):
        temp_to_state=[]
        for k in range(len(states)):
            temp_to_state.append(0)
        given_prob.append(temp_to_state)    
        given_total.append(0)
    temp_input_holder = list(inputs[i]) #Seperated string input by character
    #Tally the totality per state
    for j in range(len(states)):
        for k in range(len(temp_input_holder)-1):
            if states[j] == temp_input_holder[k]:
                given_total[j]+=1
    print(given_total)
 
    """
        #Get the state transitions 
        #Use -1 since we don't include the last character because it doesnt have a next character
        #Given prob has length of number of states. And each element is a list that is lenght of number of states
        #How to read the list 
        #[[0.5, 0.5, 0.0, 0.0], [0.5, 0.0, 0.0, 0.5], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 0.0], [0.0, 0.0, 1.0, 0.0]] 
        The first element corresponds to x given by A where x is the corresponding state of that index  # A = 0 ; C = 1 ; G = 2 ; N = 3 ; T = 4
        THe first element of the sublist of the first list is A given A
    """

    #Tallies each transition
    for j in range(len(temp_input_holder)-1): #Iteration for each character
        for k in range(len(states)): #Iteration for 
            # print(f"{states[k]} {temp_input_holder[j]}")
            if states[k]==temp_input_holder[j]:
                #Increment Value to the corresponding index of the subarray
                for l in range(len(states)):
                    if states[l] == temp_input_holder[j+1]:
                        given_prob[k][l]+=1
        
                
    #divide the total per each element in given_prob         
    
    for j in range(len(given_prob)):
        for k in range(len(given_prob[j])):
            if given_total[j] !=0:
                given_prob[j][k]=  given_prob[j][k]/given_total[j]
    print(given_prob)
    #Probability of indexes/states at sub zero
    base_val=[]
    for j in range(len(states)):
        if states[j] == temp_input_holder[0]:
            base_val.append(1)
        else:
            base_val.append(0)
    
    for j in range(no_solve):
        
        to_solve= to_solve_list[j]
        #Turn each character as an element of a list
        temp_value= list(to_solve[0])

        #Formats the values into a tuple of indexes instead of letter
        #Calling Code
        # A = 0 ; C = 1 ; G = 2 ; N = 3 ; T = 4
        # SO if we want to find Asub3 it would be represented as (0,3) 
        # for Observable H = 0 ; L = 0
        
        #converting to the format 
        for l in range(len(states)):
            if states[l]== temp_value[0]:
                to_solve[0]= (l,int(temp_value[1]))
        temp_value= list(to_solve[1])
        #converting to the format for the observable states
        for l in range(len(obs_states)):
            if obs_states[l]== temp_value[0]:
                to_solve[1]= (l, int(temp_value[1]))
    
        
        #Calculate 
        print(f"{obs_prob[to_solve[0][0]][to_solve[1][0]]} * {calculate_i(base_val,given_prob, to_solve[0])} / {calculate_o(base_val,given_prob, to_solve[1],obs_prob)}")
        result = (obs_prob[to_solve[0][0]][to_solve[1][0]] * calculate_i(base_val,given_prob, to_solve[0]) )/ calculate_o(base_val,given_prob, to_solve[1],obs_prob)
    
       
        fp.write(f"{to_solve_list_string[j]} = {result}\n")
       