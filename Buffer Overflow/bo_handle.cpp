#include <iostream>
#include <string.h>
#define MAXLEN 15
using namespace std;

void implicit(char buffer[], char danger[])
{
    memset(buffer, 0, MAXLEN);
    cout << "Implicit handling using max length" << endl;
    cout << "Input a string: ";
    int i = 0;
    char temp;
    cin.get(temp);
    while (i < MAXLEN && temp != '\n')
    {
        buffer[i] = temp;
        i++;
        cin.get(temp);
    }
    cout << "Buffer: " << buffer << endl;
    cout << "Danger: " << danger << endl;
}

void xplicit(char buffer[], char danger[])
{
    memset(buffer, 0, MAXLEN);
    cout << "Explicit handling" << endl;
    cout << "Input a string: ";
    int i = 0;
    char temp;
    cin.get(temp);
    try
    {
        while (temp != '\n')
        {
            if (i >= MAXLEN)
            {
                throw MAXLEN;
            }
            buffer[i] = temp;
            i++;
            cin.get(temp);
        }
    }
    catch (int ex)
    {
        cout << "EXCEPTION CAUGHT: Buffer overflow - User entered characters more than max length " << ex << endl;
    }
    // cin>>buffer;
    cout << "Buffer: " << buffer << endl;
    cout << "Danger: " << danger << endl;
}

int main()
{
    char danger[10] = "important";
    char buffer[MAXLEN];
    memset(buffer, 0, MAXLEN);
    cout << "Buffer address: " << &buffer << endl;
    cout << "Danger address: " << &danger << " Danger data: " << danger << endl;
    implicit(buffer, danger);
    xplicit(buffer, danger);
    return 0;
}