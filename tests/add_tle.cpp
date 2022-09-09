#include <bits/stdc++.h>

using namespace std;

int main() {
	int a, b;
	cin >> a >> b;
	int k = 0;
	for (int i = 0; i < a; i++) {
		for (int j = 0; j < b; j++) {
			for (int abc = 0; abc < 1000000; abc++) {
				k += abc;
			}
		}
	}
	cout << k << endl;
	cout << a + b << endl;
}