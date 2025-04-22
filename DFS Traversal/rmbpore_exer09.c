#include <stdio.h>
#include <stdlib.h>
#include "stack.h"
#include "graph.h"

//Implement your functions here


//Stack Functions
int isEmpty(LIST *L){ //used to check if List Head is empty
    if (L->head == NULL){
        
        return 1;
    }else{
        
        return 0;
    }
}
NODE* createNode(int data){
    NODE *head= (NODE*)malloc(sizeof(NODE)); //initialization of the head node where the "(" would be represented as 1
		head->value= data;
    return head;
}
LIST* createStack(){ //creates/initializes the List
    LIST* L= (LIST*)malloc(sizeof(LIST));
    L->head= NULL;
    return L;        
}
void push(LIST *L, NODE*node){
    node->next=L->head; // updates the new node by making the new node as the head
    L->head = node;
    return;
}
int pop(LIST *L){
        
		NODE* temp =L->head; //updates the head 
		int tempHold= L->head->value; //holder for the value to be returned
		L->head= L->head->next;
		free(temp);
		return tempHold;
        
    

}
void printStack(LIST *L){
	NODE* temp= L->head;
	while (temp!=NULL){
		printf("%d", temp->value);
		temp=temp->next;
	}
	printf("\n");
}

//GRAPH FUNCTIONS

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
void insertEdge(GRAPH *G, int u, int v){
	G->matrix[u][v]=1; //put u to v as 1
	G->matrix[v][u]=1; //put v to u as 1

}

int *createVisited(GRAPH *G){
	int *visited= (int*)malloc(sizeof(int)*G->num_vertices); //allocate memory for the visited array
	
	for(int i = 0; i<G->num_vertices;i++){ //marks all element of the array as not visited which is 0
		visited[i]=0; //representation for not visited
	}
	return visited;
}
void dfs(GRAPH *G, int start){
	int *visited=createVisited(G); //creates the visited array
	LIST *s= createStack(); //creates the temporary stack
	
	
	push(s,createNode(start)); //push the starting vertice
	while(isEmpty(s)!=1){
		
		int current =pop(s); //pop the current vertice

		if(visited[current]==0){ //condition only occurs if node is not visited 
		printf("%d ", current+1);	//print the vertex
		visited[current]=1;	//mark as visited the current vertex
		for(int j=0;j<G->num_vertices;j++){
			if(visited[j]==0 && G->matrix[current][j]==1){
				push(s,createNode(j)); //push the adjacent vertices that is not visited
			}
		}
		}
		
	}
	free(visited); //free used array
	free(s); //free the stack
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
	int vertices, lines, u, v;

	scanf("%d", &vertices);
	GRAPH *G = createGraph(vertices);

	while(1) {
		scanf(" %c", &command);

		switch(command) {
			case '+':
				scanf(" %d %d", &u, &v);
				insertEdge(G, u-1, v-1); //there's a -1 since we use 0-indexing in the arrays
				printf("Successfully inserted edge %d %d\n", u, v);
				break;
			case '#':
				printf("\nDFS: ");
				dfs(G, 0); //0 is the initial value since we use 0-indexing (it still represents vertex 1)
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