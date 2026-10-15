You are given an `n x n` integer matrix `grid` where `grid[i][j]` is the elevation of that cell. At time `t` the water level is `t`, and you may step between 4-directionally adjacent cells only when both have elevation at most `t`. You can swim any distance instantly, and you start at the top-left cell at time 0.

Return the least time at which you can reach the bottom-right cell.

Constraints:
- `1 <= n <= 50`
- `grid` contains each value in `0..n*n-1` exactly once
