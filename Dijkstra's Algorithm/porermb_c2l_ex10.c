// Richmond Michael B. Pore
// C-2L
// This code is used to finds the shortest path from point A and point B in a graph

#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

//Implement your functions here

GRAPH *createGraph(int vertices){
	GRAPH* G= malloc(sizeof(GRAPH)); //allocate memory for the graph
	
	//2d array allocation
	G->matrix=(int**)malloc(sizeof(int*)*vertices);
	for(int i=0; i<vertices;i++){
		G->matrix[i]= (int*)malloc(sizeof(int)*vertices);
	} 

	//setting all values to zero
	for(int j=0;j<vertices;j++){
		for(int k=0;k<vertices;k++){
			G->matrix[j][k]=0;
			//printf("%d", G->matrix[j][k]);
		}
	}
	
	G->num_vertices= vertices;
	return G;
}
void insertEdge(GRAPH *G, int u, int v,int w){
	G->matrix[u][v]=w; //put u to v as 1


}
int *createVisited(GRAPH *G){
	int *visited= (int*)malloc(sizeof(int)*G->num_vertices); //allocate memory for the visited array
	
	for(int i = 0; i<G->num_vertices;i++){ //marks all element of the array as not visited which is 0
		visited[i]=0; //representation for not visited
	}
	return visited;
}

int *createDistance(GRAPH *G){
	int *distance= (int*)malloc(sizeof(int)*G->num_vertices); //allocate memory for the visited array
	
	for(int i = 0; i<G->num_vertices;i++){ //marks all element of the array as not visited which is 0
		distance[i]=99999; //representation for not visited
	}
	return distance;
	
}
int *createParent(GRAPH *G){
	int *parent= (int*)malloc(sizeof(int)*G->num_vertices); //allocate memory for the visited array
	
	for(int i = 0; i<G->num_vertices;i++){ //marks all element of the array as not visited which is 0
		parent[i]=-1; //representation for not visited
	}
	return parent;
}
int checkifVisited(int* visited, int num_vertices){
	for(int i=0; i<num_vertices; i++){
		if(visited[i]==0){
			return 0;
		}
	}
	return 1;
}
void dijkstra(GRAPH *G, int source, int target){
	int currentdistance=0;
	//initialize the needed arrays
	int*visited=createVisited(G);
	int *distance= createDistance(G);
	int *parent= createParent(G);
	
	distance[source]=0; //set source vertex distance to 0
	int u =0;
	
	while(checkifVisited(visited, G->num_vertices)==0 ){
		
		for(int m=0; m<G->num_vertices;m++){ //gets the first index that is not visited since u can bypass the second loop where it finds the minimum
		//becuase its assumed that u is not a visited node
			if(visited[m]==0){
				u=m;
			}
		}
		
		

		for (int i = 0; i<G->num_vertices;i++){
			//printf("%d  %d \n", distance[i], visited[i]);
			//printf("[%d]%d %d %d \n",i,visited[i],  u, distance[i]);
			if(visited[i]==0 && distance[u]>=distance[i]){ //finds the minimum distance that is not visited
				u=i;  
					
			}
		}
		if(distance[u]==99999){// break if the current uand its minimum distancei s 99999
			
			break;
		}
		currentdistance= distance[u];		
		//printf("my u %d \n", u);
		visited[u]= 1; //set u index as visited
		
		
		
		//updates the distance and parents
		for(int j = 0 ; j<G->num_vertices;j++){
			if(G->matrix[u][j]!=0 && visited[j]!=1){ //updates the distance of the vertices that are adjacent to u
				if(G->matrix[u][j]+ currentdistance<distance[j]){ //replace the distance if its less than current distance
					distance[j]=G->matrix[u][j]+ currentdistance; //set distance
					parent[j]=u; //set the parent to current vertex
				}
					
				
				
			}
		}
		
		

		
		
		
	}



	int  temp_target=target;
	int final_arrsize=0;
	//checks what is the size of the path
	while(temp_target!=-1){
		final_arrsize++;
		if(parent[temp_target]==-1 && temp_target!=source){ // prints this prompt if there is no path for the given source and target and returns
			printf("PATH FRPM %d to %d: IMPOSSIBLE \n", source+1,target+1);
			printf("DISTANCE FROM %d to %d: -1\n", source+1,target+1);
			return;
		}
		temp_target= parent[temp_target];


	}

	
	//updates the array
	printf("PATH FROM %d to %d:", source+1, target+1);
	int *final_array = (int*)malloc(sizeof(int)*final_arrsize);
	for(int l=final_arrsize; l>0;l--){
		final_array[l-1]= target+1;
		target=parent[target];
	}

	//prints the array
	for(int p = 0 ; p<final_arrsize; p++){
		printf("% d", final_array[p]);
	}
	printf("\nDISTANCE FROM %d to %d: %d", source+1, target+1,currentdistance);
	
	// free arrays that were made in this function
	free(final_array);
	free(visited);
	free(parent);
	free(distance);
	
}

void printMatrix(GRAPH *G){
	//2d array printing	
	for(int j=0;j<G->num_vertices;j++){
		
		for(int k=0;k<G->num_vertices;k++){
			printf("%d	",G->matrix[j][k]);
		}
		printf("\n");
	}
}

void freeMatrix(GRAPH *G){
	//frees all matrix
	for(int j=0;j<G->num_vertices;j++){
		free(G->matrix[j]);
		
	}
}
int main() {
	char command;
	int vertices, lines, u, v, w, source, target;

	scanf("%d", &vertices);
	GRAPH *G = createGraph(vertices);

	while(1) {
		scanf(" %c", &command);

		switch(command) {
			case '+':
				scanf(" %d %d %d", &u, &v, &w);
				insertEdge(G, u-1, v-1, w); //there's a -1 since we use 0-indexing in the arrays
				printf("Successfully inserted edge %d %d\n", u, v);
				break;
			case '#':
				scanf(" %d %d", &source, &target);
				dijkstra(G, source-1, target-1);
				printf("\n");
				break;
			case 'p':
				printf("\nADJACENCY MATRIX: \n");
				printMatrix(G);
				break;
			case 'Q':
				freeMatrix(G);
				free(G);
				return 0;
			default:
				printf("Unknown command: %c\n", command);
		}
	}
}