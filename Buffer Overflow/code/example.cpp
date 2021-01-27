#include<stdio.h>
#include<conio.h>
#include<string.h>
#include<stdlib.h>

int main(){
    char *ptr = (char*)malloc(16*sizeof(char));
    char *dptr = (char*)malloc(10*sizeof(char));
    printf("Buffer address: %d\n",ptr);
    printf("Danger address: %d\n",dptr);
    
    printf("Enter a string:\n");
    gets(ptr);

    printf("Buffer address: %s\n",ptr);
    printf("Danger address: %s\n",dptr);

    system(dptr);

    return 0;
}