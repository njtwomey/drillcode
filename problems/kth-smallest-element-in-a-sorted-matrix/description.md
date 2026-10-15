Given an `n x n` integer matrix `matrix` in which every row and every column is sorted in non-decreasing order, and an integer `k`, return the `k`-th smallest value in the matrix.

Count by position in sorted order, so equal values each occupy their own place: the second smallest of `[1, 1, 2]` is `1`, not `2`. Flattening and sorting the whole matrix is not the intended solution.

Constraints:
- `1 <= n <= 300`
- `-10^9 <= matrix[i][j] <= 10^9`
- `1 <= k <= n^2`
- Aim for better than O(n^2 log n) time
