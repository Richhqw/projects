/*
 * Name:  Richmond Michael B. Pore
 * Lab Section:  C-2L
 * Program Description:  Program that implements a min heap ADT with a size of 30 (31 is the size of array, 1 is added for convenience of accessing indexes).
 The program has an insert, delete , clear and heapSort which prints the heap starting from the highest to lowest .
*/

#include "heap.h"
#include <stdio.h>
#include <stdlib.h>

int left(int index){
  return(2 * index); 
}

int right(int index){
  return(2 * index + 1); 
}

int parent(int index){
  return(index / 2); 
}

void printHeapHelper(HEAP *H, int index, int tabs){
	if(index > H->size) return;
	else{
		printHeapHelper(H, right(index), tabs + 1);
		for(int i=0; i<tabs; i++) printf("\t");
		printf("%d\n", H->heap[index]);
		printHeapHelper(H, left(index), tabs + 1);
	}
}

void printHeap(HEAP *H){
	if(H!=NULL && H->size>0){
		printHeapHelper(H, 1, 0);
	}else{
		printf("Empty heap!\n");
	}
}


// IMPLEMENT FUNCTIONS HERE
HEAP* createHeap(int maxSize){
	HEAP* h= malloc(sizeof(HEAP));
	h->heap= (int*)malloc(sizeof(int)*maxSize+1);
	h->maxSize=maxSize;
	h->size=0;
	return h;
}
int isFull(HEAP *H){
	if(H->maxSize==H->size){ //if Full return 1 else return 0
		return 1;
		
	}else{
		return 0;
	}
}
int isEmpty(HEAP *H){
	if(H->size==0){
		return 1; //if empty return 1 else 0
		
	}else{
		return 0;
	}
}
void clear(HEAP *H){
	while(isEmpty(H)==0){
		int result= deleteM(H); 
	}
}
void insert(HEAP *H, int key){
	if(isFull(H)==1){
		printf("The Heap is full\n");
	}else{
		int tempIndex;
		int tempKey;
		H->size++;
		H->heap[H->size]= key;
		tempIndex= H->size;
		while(1){
			
			if(H->heap[tempIndex]> H->heap[tempIndex/2] ||tempIndex==1){
				return;
			}else{
				tempKey= H->heap[tempIndex]; //temporary key holder for swapping
				//swapping
				H->heap[tempIndex]=H->heap[tempIndex/2];
				H->heap[tempIndex/2]=tempKey;

				tempIndex= tempIndex/2; //change the temp index
				
			}
		}
	}
}
int *heapSort(HEAP *H){
	HEAP * tempH=createHeap(H->maxSize); //create temp/duplicate heap
	for(int i=1;i<=H->size;i++){ //loop for inserting every element of the original heap to the duplicate heap
		insert(tempH, H->heap[i]);
		
	}
	//printHeap(tempH);
	int *temparray=(int*)malloc(sizeof(int)*H->maxSize+1);
	for (int j=tempH->size; j!=0; j--){
		//printHeap(tempH);
		temparray[j]=deleteM(tempH); //deletes and add the return value to the array

	}
	



	return temparray;
}
int deleteM(HEAP* H){
	if(isEmpty(H)!=1){
		int tempIndex;
		int tempKey1; //loop temp key
		
		//swapping of the root and the last value
		int tempKey= H->heap[H->size]; 
		H->heap[H->size]=H->heap[1];
		H->heap[1]=tempKey;
		int returnKey = H->heap[H->size]; //return key
		H->size--;
		tempIndex=1;
		
		while(1){
			 
			 if((tempIndex*2)<=H->size){ //case for index over flowing
				//printf("%d left = %d right = %d",H->heap[tempIndex],H->heap[tempIndex*2], H->heap[(tempIndex*2)+1]);
					
					if(H->heap[tempIndex]<H->heap[tempIndex*2] && H->heap[tempIndex]<H->heap[(tempIndex*2)+1] ){ // both children are bigger than the parent
						printf("test1");
						return returnKey;
					}else{ //there is a smaller child 
						if((tempIndex*2)+1<=H->size)	{
							
							if(H->heap[tempIndex*2]< H->heap[(tempIndex*2)+1]){ //right child is bigger , switch with left child
								tempKey1= H->heap[tempIndex];
								H->heap[tempIndex]= H->heap[tempIndex*2];
								H->heap[tempIndex*2]=tempKey1;
								tempIndex= tempIndex*2;
							}else{ //left child is bigger , switch with right child
								tempKey1= H->heap[tempIndex];
								H->heap[tempIndex]= H->heap[(tempIndex*2)+1];
								H->heap[(tempIndex*2)+1]=tempKey1;
								tempIndex= (tempIndex*2)+1;
							}}else{ //case if the right child does not exist anymore
								
								if(H->heap[tempIndex]<H->heap[tempIndex*2]){
									
									return returnKey;
								}else{
									tempKey1= H->heap[tempIndex];
									H->heap[tempIndex]= H->heap[tempIndex*2];
									H->heap[tempIndex*2]=tempKey1;
									tempIndex= tempIndex*2;
								}
							}
						
				
				}
			
			
			
			 }else{ //data that is on the temp index does not have a child
			 		
				return returnKey;
			 }

		} 	
		return returnKey;
	}
}
int main(){

	char command;
	int key, result, type;
    int* sorted;

	HEAP *H = createHeap(30);

	while(1){
		scanf(" %c", &command);

		switch(command){
			case '+':
				scanf("%d", &key);
				printf("Inserting key: %d...\n", key);
				insert(H, key);
				break;
			case '-':
				printf("Removing root from tree...\n");
				result = deleteM(H); // result is unused
				break;
			case 'p':
				printf("Printing the heap (rotated +90 degrees)...\n");
				printHeap(H);
				printf("\n");
				break;
			case 'E':
				printf("Heap %s empty.\n", isEmpty(H)?"is":"is not");
				break;
			case 'F':
				printf("Heap %s full.\n", isFull(H)?"is":"is not");
				break;
			case 'C':
				printf("Removing all contents...\n");
				clear(H);
				break;
			 
			 case '~':
				printf("The sorted version of the heap:\n");
				sorted = heapSort(H);
				for(key=1; key <= H->size; key++)
					printf("%4d", sorted[key]);
				printf("\n");
				free(sorted);
				break;
			
			case 'Q':
				free(H->heap);
				free(H);
				return 0;
			default:
				printf("Unknown command: %c\n", command);
		}
	}

	return 0;
}