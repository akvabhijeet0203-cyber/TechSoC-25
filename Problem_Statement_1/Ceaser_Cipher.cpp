#include <iostream>
#include <string>
using namespace std;

int main() {
    int sv;
    cout << "Enter shift value (+ve for Encode, -ve for Decode): ";
    cin >> sv;

    cin.ignore(); // clear buffer
    cout << "Enter the line to be coded: ";
    string ip, op = "";
    getline(cin, ip);

    sv = sv % 26; // normalizing shift

    for (char ch : ip) {
        if (ch >= 'a' && ch <= 'z')
            ch = 'a' + (ch - 'a' + sv + 26) % 26;
        else if (ch >= 'A' && ch <= 'Z')
            ch = 'A' + (ch - 'A' + sv + 26) % 26;

        op += ch;
    }

    cout << "OUTPUT: " << op << endl;
    return 0;
}

