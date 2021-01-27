#include <iostream>
#include <string.h>
#include<stdlib.h>
#define MAXLEN 10
using namespace std;

int main()
{
    cout<<"Form example to demonstrate buffer overflow"<<endl;
    char *password = (char*)malloc(MAXLEN*sizeof(char));
    char *email = (char*)malloc(MAXLEN*sizeof(char));
    char *name = (char*)malloc(MAXLEN*sizeof(char));
    cout<<"Address of name buffer: "<<&name<<endl;
    cout<<"Address of email buffer: "<<&email<<endl;
    cout<<"Address of password buffer: "<<&password<<endl;
    cout<<"Enter name: ";
    cin>>name;
    cout<<"Enter email: ";
    cin>>email;
    cout<<"Enter password: ";
    cin>>password;

    cout<<"Name: "<<name<<endl;
    cout<<"Email: "<<email<<endl;
    cout<<"Password: "<<password<<endl;
    
    return 0;
}