Given an `m x n` integer grid `matrix`, return the length of the longest strictly increasing path through it. From a cell you may move up, down, left or right to an adjacent cell; diagonal moves and moving outside the grid are not allowed. The path may start at any cell, and each step must land on a larger value than the previous one.

Constraints:
- `1 <= m, n <= 200`
- `0 <= matrix[i][j] <= 2^31 - 1`
- Re-exploring paths from every cell without sharing work is exponential
