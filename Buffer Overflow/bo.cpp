#include<stdio.h>
#include<conio.h>
#include<iostream>
using namespace std;

int main(){
    char danger[10] = "important";
    char buffer[15];
    cout<<"Buffer address: "<<&buffer<<endl;
    cout<<"Danger address: "<<&danger<<" Danger data: "<<danger<<endl;
    cout << "Input a string: ";
    cin>>buffer;
    cout<<"Buffer: "<<buffer<<endl;
    cout<<"Danger: "<<danger<<endl;
    return 0;
}