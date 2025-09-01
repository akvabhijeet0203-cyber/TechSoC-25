#include <iostream>
using namespace std;

int main() {
    char cipher[200];   // input message (max 200 characters)
    cout << "Enter the encoded message (small letters only): ";
    cin.getline(cipher, 200);   // read input

    int bestShift = 0;
    int bestScore = -1;
    char bestText[200];

    // find length of cipher (manual count, no strlen)
    int len = 0;
    while (cipher[len] != '\0') {
        len++;
    }

    // Try all shifts from 1 to 25
    for (int shift = 1; shift <= 25; shift++) {
        char decoded[200];
        int vowelCount = 0;

        // decode each character
        for (int i = 0; i < len; i++) {
            char ch = cipher[i];

            if (ch >= 'a' && ch <= 'z') {
                char newChar = (ch - 'a' - shift + 26) % 26 + 'a';
                decoded[i] = newChar;

                // count vowels
                if (newChar == 'a' || newChar == 'e' || newChar == 'i' ||
                    newChar == 'o' || newChar == 'u') {
                    vowelCount++;
                }
            }
            else {
                decoded[i] = ch; // keep spaces and punctuation same
            }
        }
        decoded[len] = '\0';  // end string

        // choose the best shift (max vowels)
        if (vowelCount > bestScore) {
            bestScore = vowelCount;
            bestShift = shift;

            // copy decoded into bestText
            for (int j = 0; j < len; j++) {
                bestText[j] = decoded[j];
            }
            bestText[len] = '\0';
        }
    }

    cout << "Best shift found: " << bestShift << endl;
    cout << "Decrypted message: " << bestText << endl;

    return 0;
}

