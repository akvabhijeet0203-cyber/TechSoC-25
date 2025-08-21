#include<iostream>
#include<string>
using namespace std;

const double e = 2.718281828;
const double PI = 3.1415926535;

double power(double num, int p) {
    double res = 1;
    for (int i = 0; i < p; i++) res *= num;
    return res;
}

double abso(double x) { return (x < 0) ? -x : x; }

long fact(int x) {
    long pro = 1;
    while (x > 1) {
        pro *= x;
        x--;
    }
    return pro;
}
/**
bool hasDecimal(double num) {
    return num != (int)num;
This fails for numbers like 3.0000000001 due to floating-point errors.
}
*/
bool hasDecimal(double num) {
    return abso(num - (int)num) > 1e-9;
}


// Taylor series for ln(x) near 1
double lnNear1(double cnum) {
    double result = 0;
    int cnt = 1;
    double z = cnum - 1;
    double y;
    do {
        double sign = (cnt % 2 == 0) ? -1 : 1;
        y = sign * power(z, cnt) / cnt;
        result += y;
        cnt++;
    } while (abso(y) > 1e-10);
    return result;
}

double ln(double num) {
    if (num == 0) { cout << "NOT DEFINED"; return 0; }
    else if (num < 0) { cout << "Invalid Input"; return 0; }
    int k = 0;
    while (num > 1.5) { num /= e; k++; }
    while (num < 0.5) { num *= e; k--; }
    return k + lnNear1(num);
}

double exp_(double x) {
    int cnt = 1;
    double term = 1, sum = 1;
    do {
        term *= x / cnt;
        sum += term;
        cnt++;
    } while (abso(term) > 1e-12);
    return sum;
}

double log10_(double x) {
    return ln(x) / ln(10);
}

double mySqrt(double x) {
    if (x < 0) {
        cout << "Error: Square root of negative number!" << endl;
        return 0;
    }
    double guess = x / 2.0;
    for (int i = 0; i < 100; i++) {
        guess = (guess + x / guess) / 2.0; // Newton-Raphson
    }
    return guess;
}

double deciPow(double a, double b) {
    if (a <= 0) {
        cout << "Invalid input for power!" << endl;
        return 0;
    }
    return exp_(b * ln(a));
}

double normalize(double x) {
    while (x > 2*PI) x -= 2*PI;
    while (x < -2*PI) x += 2*PI;
    return x;
}

double sin_(double x) {
    x = normalize(x);
    double term = x, sum = x;
    int n = 1;
    while (abso(term) > 1e-10) {
        term *= -1 * x * x / ((2 * n) * (2 * n + 1));
        sum += term;
        n++;
    }
    return sum;
}

double cos_(double x) {
    x = normalize(x);
    double term = 1, sum = 1;
    int n = 1;
    while (abso(term) > 1e-10) {
        term *= -1 * x * x / ((2 * n - 1) * (2 * n));
        sum += term;
        n++;
    }
    return sum;
}

double tan_(double x) {   
    x = normalize(x);
    double c = cos_(x);
    if (abso(c) < 1e-12) {
        cout << "Error: Tan undefined at this angle!" << endl;
        return 0;
    }
    return sin_(x) / c;
}
double arcsin(double x) {
    if (x < -1 || x > 1) {
        cout << "Invalid input for arcsin!" << endl;
        return 0;
    }
    double term = x, sum = x;
    int n = 1;
    while (abso(term) > 1e-12) {
        term *= (x*x) * (2*n-1)*(2*n-1) / ( (2*n)*(2*n+1) );
        sum += term;
        n++;
    }
    return sum;
}

double arccos(double x) {
    if (x < -1 || x > 1) {
        cout << "Invalid input for arccos!" << endl;
        return 0;
    }
    return PI/2 - arcsin(x);
}

double arctan(double x) {
    if (x > 1) return PI/2 - arctan(1/x);
    if (x < -1) return -PI/2 - arctan(1/x);
    double term = x, sum = x;
    int n = 1;
    while (abso(term) > 1e-12) {
        term *= -(x*x) * (2*n-1) / (2*n+1);
        sum += term;
        n++;
    }
    return sum;
}
int main() {
    int choice;
    double num1, num2, result;

    do {
        cout << "\n========= SCIENTIFIC CALCULATOR =========\n";
        cout << " 1. Addition (+)\n";
        cout << " 2. Subtraction (-)\n";
        cout << " 3. Multiplication (*)\n";
        cout << " 4. Division (/)\n";
        cout << " 5. Power (a^b)\n";
        cout << " 6. Square Root (sqrt)\n";
        cout << " 7. Natural Logarithm (ln)\n";
        cout << " 8. Logarithm base 10 (log10)\n";
        cout << " 9. Exponential (e^x)\n";
        cout << "10. Sine (sin)\n";
        cout << "11. Cosine (cos)\n";
        cout << "12. Tangent (tan)\n";
        cout << "13. Arcsine (arcsin)\n";
        cout << "14. Arccosine (arccos)\n";
        cout << "15. Arctangent (arctan)\n";
        cout << "16. Exit\n";
        cout << "=========================================\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:  // Addition
                cout << "Enter two numbers: ";
                cin >> num1 >> num2;
                result = num1 + num2;
                cout << "Result: " << result << endl;
                break;

            case 2:  // Subtraction
                cout << "Enter two numbers: ";
                cin >> num1 >> num2;
                result = num1 - num2;
                cout << "Result: " << result << endl;
                break;

            case 3:  // Multiplication
                cout << "Enter two numbers: ";
                cin >> num1 >> num2;
                result = num1 * num2;
                cout << "Result: " << result << endl;
                break;

            case 4:  // Division
                cout << "Enter two numbers: ";
                cin >> num1 >> num2;
                if (num2 == 0)
                    cout << "Error: Division by zero!\n";
                else
                    cout << "Result: " << num1 / num2 << endl;
                break;

            case 5:  // Power
                cout << "Enter base and exponent: ";
                cin >> num1 >> num2;
                if (hasDecimal(num2))
                    result = deciPow(num1, num2);
                else
                    result = power(num1, (int)num2);
                cout << "Result: " << result << endl;
                break;

            case 6:  // Square root
                cout << "Enter number: ";
                cin >> num1;
                cout << "Result: " << mySqrt(num1) << endl;
                break;

            case 7:  // ln
                cout << "Enter number: ";
                cin >> num1;
                cout << "Result: " << ln(num1) << endl;
                break;

            case 8:  // log10
                cout << "Enter number: ";
                cin >> num1;
                cout << "Result: " << log10_(num1) << endl;
                break;

            case 9:  // exp
                cout << "Enter power of e: ";
                cin >> num1;
                cout << "Result: " << exp_(num1) << endl;
                break;

            case 10:  // sin
                cout << "Enter angle (radians): ";
                cin >> num1;
                cout << "Result: " << sin_(num1) << endl;
                break;

            case 11:  // cos
                cout << "Enter angle (radians): ";
                cin >> num1;
                cout << "Result: " << cos_(num1) << endl;
                break;

            case 12:  // tan
                cout << "Enter angle (radians): ";
                cin >> num1;
                cout << "Result: " << tan_(num1) << endl;
                break;

            case 13:  // arcsin
                cout << "Enter value (-1 <= x <= 1): ";
                cin >> num1;
                cout << "Result: " << arcsin(num1) << endl;
                break;

            case 14:  // arccos
                cout << "Enter value (-1 <= x <= 1): ";
                cin >> num1;
                cout << "Result: " << arccos(num1) << endl;
                break;

            case 15:  // arctan
                cout << "Enter value: ";
                cin >> num1;
                cout << "Result: " << arctan(num1) << endl;
                break;

            case 16:
                cout << "Exiting program. Goodbye!\n";
                break;

            default:
                cout << "Invalid choice! Please try again.\n";
        }
    } while (choice != 16);

    return 0;
}
/**
int main() {
    double num1, num2, result;
    char op;

    cout << "Enter expression (e.g., 5 + 3 OR 2 ^ 3): ";
    cin >> num1 >> op;

    if (op == '+' || op == '-' || op == '*' || op == '/' || op == '^') {
        cin >> num2;
    }

    switch (op) {
        case '+': result = num1 + num2; break;
        case '-': result = num1 - num2; break;
        case '*': result = num1 * num2; break;
        case '/':
            if (num2 != 0) result = num1 / num2;
            else { cout << "Error: Division by zero!\n"; return 0; }
            break;
        case '^':
            if (hasDecimal(num2)) result = deciPow(num1, num2);
            else result = power(num1, (int)num2);
            break;
        default:
            cout << "Invalid operator!\n";
            return 0;
    }

    cout << "OUTPUT: " << result << endl;
    return 0;
}
*/
