#include <iostream>
#include <string.h>
#include<stdlib.h>
using namespace std;

int recurse(int *top,int n){
    if(n<=0){
        return n;
    }
    cout<<"Storing on stack - local variable n="<<n<<endl;
    *top = n;
    top++;
    cout<<"Address of stack top "<<top<<endl;
    return n+recurse(top,n-1);
}

int main(){
    int *stack_ptr = (int*)malloc(10*sizeof(int));
    int *top = stack_ptr;
    int *flag_ptr = (int*)malloc(sizeof(int));
    *flag_ptr = 0;
    cout<<"Address of flag variable: "<<flag_ptr<<endl;
    cout<<"Contents of flag variable: "<<*flag_ptr<<endl;
    cout<<"Address of stack start: "<<stack_ptr<<endl;
    cout<<"Address of stack top "<<top<<endl;

    int n;
    cout<<"Enter a number: "<<endl;
    cin>>n;
    cout<<"Calling recursive sum function..."<<endl;
    int ans = recurse(top,n);
    cout<<"Result of recursion: "<<ans<<endl;
    cout<<"Address of stack top: "<<top<<endl;
    cout<<"Contents of flag variable: "<<*flag_ptr<<endl;
    return 0;
}