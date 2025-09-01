#include <iostream>
using namespace std;

int main() {
    char cipher[200];   // input message (max 200 chars)
    cout << "Enter the encoded message (use only small letters and spaces): ";
    cin.getline(cipher, 200);   // input

    int bestShift = 0;
    int bestScore = -1;
    char bestText[200];

    // Try all shifts from 1 to 25
    for (int shift = 1; shift <= 25; shift++) {
        char decoded[200];
        int vowelCount = 0;

        // decode each character
        for (int i = 0; cipher[i] != '\0'; i++) {
            char ch = cipher[i];

            if (ch >= 'a' && ch <= 'z') {
                char newChar = (ch - 'a' - shift + 26) % 26 + 'a';
                decoded[i] = newChar;

                // check if vowel
                if (newChar == 'a' || newChar == 'e' || newChar == 'i' ||
                    newChar == 'o' || newChar == 'u') {
                    vowelCount++;
                }
            }
            else {
                decoded[i] = ch; // keep space same
            }
        }
        decoded[strlen(cipher)] = '\0'; // end the string

        // if this has more vowels, update best
        if (vowelCount > bestScore) {
            bestScore = vowelCount;
            bestShift = shift;

            // copy decoded into bestText
            for (int j = 0; decoded[j] != '\0'; j++) {
                bestText[j] = decoded[j];
            }
            bestText[strlen(cipher)] = '\0';
        }
    }

    cout << "Best shift found: " << bestShift << endl;
    cout << "Decrypted message: " << bestText << endl;

    return 0;
}

