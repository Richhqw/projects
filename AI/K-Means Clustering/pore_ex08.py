import re
import random

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from tkinter.filedialog import askdirectory
def plot3d(statistics_data,k):
    #Assign a list colors of sign 10 since it is the maximum number of cluster the program can support
    colors =['blue', 'violet', 'yellow', 'gray', 'brown', 'teal', 'magenta', 'purple', 'navy', 'lime']

    #initialize lists
    main_list= []
    for i in range(k):
        main_list.append([])
    for i in range(len(statistics_data)):
        main_list[statistics_data[i][0]].append((statistics_data[i][3],statistics_data[i][4],statistics_data[i][5]))
    
   
    
    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(main_list)):
        for point in main_list[i]:
            # print(f"{point[0]} {point[1]} {point[2]}")
            ax.scatter(point[0], point[1], point[2], c=colors[i], marker='o') # Plots the point
    

    # Label 
    ax.set_xlabel('Points Per Game')
    ax.set_ylabel('Assist Per Game')
    ax.set_zlabel('Rebounds Per Game')

    # Display the plot
    plt.show()
def outputwrite(statistics_data,loc,k,initial_centroids,final_centroids,iteration):

    new_loc= re.split('/',loc)
    f= open("output.txt", "w")
    f.write(f"K-Means Clustering Output from {new_loc[-1]}/players_stat.csv")
    f.write("\n")
    f.write(f"k = {k}")
    f.write("\n")
    f.write("Initial Centrouds\n")
    for i in range(len(initial_centroids)):
        f.write(f"[{initial_centroids[i][1]},{initial_centroids[i][2]},{initial_centroids[i][3]}]")
        f.write("\n")
    f.write("Final Centroids\n")
   
    for i in range(len(final_centroids)):
        f.write(f"[{final_centroids[i][0]},{final_centroids[i][1]},{final_centroids[i][2]}]")
        f.write("\n")
    f.write(f"Iterations: {iteration+1}\n")
    for i in range(len(statistics_data)):
        f.write(f"{statistics_data[i][0]} : {statistics_data[i][2]} - {statistics_data[i][1]}\t\t[{statistics_data[i][3]},{statistics_data[i][4]},{statistics_data[i][5]},]")
        f.write("\n")
    pass
loc=askdirectory()
data=open(loc+"/players_id.csv",'r',encoding='utf-8-sig')

data_key={}

statistics_data=[]
for line in data:
    line_holder = re.split(',|\n',line)
    data_key[line_holder[0]]=line_holder[1]

statistics_datafile= open(loc+"/players_stat.csv",'r',encoding='utf-8-sig')
for line in statistics_datafile:
    # print(line)
    line_holder = re.split(',|\n',line)
    if(line_holder[-1]==''):
        line_holder.pop(-1)
    line_holder = [int(element) for element  in line_holder]
    

    statistics_data.append(line_holder)
#Initialize Centroids
while 1:
    k= int(input("Enter K value (1-10): "))
    if k>=1 and k<=10:
        break
    else: 
        print("Not a valid integer")
index_rand=[]
for i in range(k):
    while 1:
        val = random.randint(0,len(statistics_data))
        if val not in index_rand:
            index_rand.append(val)
            break
#Convert the Indexes to their value in the statistical_data list

for i in range(len(index_rand)):
    index_rand[i]=statistics_data[index_rand[i]]
print(index_rand)
index_rand= [statistics_data[403],statistics_data[176],statistics_data[465],statistics_data[418],statistics_data[300],statistics_data[163]]
initial_centroids=[]
for i in range(len(index_rand)):
    initial_centroids.append(index_rand[i].copy())
print(initial_centroids)
# for i in range(len(index_rand)):
#     initial_centroids[i].pop(0)
#Calculate
temp=0 
cond= 1
while cond==1:
    print(f'Iteration={temp}')
    #lists follows the indexing of statistical_data
    class_data=[] #stores their class
    distance_data=[] #stores the distance
    for data_curr in range(len(statistics_data)):
        index_rand_distance=[]
        #stores the distance for each cluster per data
        for centroids in index_rand:
            
          
            sum=0
            #Compute for each distance value of Data for each point
            for i in range(1,len(statistics_data[0])):
                
                sum += (statistics_data[data_curr][i]-centroids[i])**2
            index_rand_distance.append((sum)**(1/2))
        
        lowest_val_index= 0
         
        # print(index_rand_distance)
        #Finds the smallest distance from the clusters and appends that cluster index in class_data
        for i in range(len(index_rand_distance)):
            if  index_rand_distance[i] < index_rand_distance[lowest_val_index]:
                lowest_val_index=i
        class_data.append(lowest_val_index)

    # print(class_data)


        
    #Recalculate Centroid
    #Initialize the list
    new_centroid=[]
    total=[]
    for j in range(len(index_rand)):
        temp_centroid=[]
        total.append(0)
        for i in range(len(statistics_data[0])):
            temp_centroid.append(0)
        new_centroid.append(temp_centroid)

    #Computation proper for the Centroids
    for i in range(len(statistics_data)):
        temp_holder = statistics_data[i].copy() # copy content of array
        
        # print(temp_holder)
        total[class_data[i]]= total[class_data[i]]+1 #Increment count for that class
        for j in range(1,len(temp_holder)):
            
            new_centroid[class_data[i]][j]= new_centroid[class_data[i]][j] + temp_holder[j]
    

    
    #divide to the total
    for i in range(len(new_centroid)):
        for j in range(len(new_centroid[0])):
            new_centroid[i][j]= new_centroid[i][j]/total[i]
    #Increment Temp which is used for counting iteration
    temp=temp+1
    #Check if old centroid is same as new one:
    cond=0
    for i in range(len(index_rand)):
        for j in range(1,len(index_rand[0])):
            if new_centroid[i][j]!= index_rand[i][j]:
                # print(f"{new_centroid[i][j]} and {index_rand[i][j]}")
                cond=1
                break
    index_rand=new_centroid
    


#Edit statistic_data to prepare for file writing
for i in range(len(statistics_data)):
    if str(statistics_data[i][0]) in data_key.keys():
       
        statistics_data[i].insert(0,data_key[str(statistics_data[i][0])])
        statistics_data[i].insert(0,class_data[i])
    else:
        statistics_data[i].insert(0,"N/A")
        statistics_data[i].insert(0,class_data[i])
    
print(statistics_data[0])
#Clean index_rand to remove the 1st element
for i in range(len(index_rand)):
    index_rand[i].pop(0)
print("test")
print(initial_centroids)
outputwrite(statistics_data,loc,k,initial_centroids,index_rand,temp)
plot3d(statistics_data,k)