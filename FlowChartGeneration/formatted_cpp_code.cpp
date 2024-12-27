#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int main() {

  int x;
  int y;
  cin >> x >> y;
  cout << x << y << endl;

  for (int i = 0; i < 3; i++)
    cout << i + 1 << '\n';

  vector<int> vec(5);
  std::for_each(vec.begin(), vec.end(), [](int x) { std::cout << x << " "; });
}