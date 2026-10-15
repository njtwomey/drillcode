There are `n` cities. `isConnected` is an `n x n` matrix where `isConnected[i][j] == 1` means cities `i` and `j` are directly connected, and `0` means they are not. Connections are mutual, and every city is connected to itself.

A province is a maximal group of cities that are connected directly or through other cities. Return the number of provinces.

Constraints:
- `1 <= n <= 200`
- `isConnected` is symmetric and `isConnected[i][i] == 1`
