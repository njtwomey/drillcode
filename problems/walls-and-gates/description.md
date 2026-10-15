You are given a grid `rooms` where `-1` is a wall, `0` is a gate, and `2147483647` (call it INF) is an empty room. Fill every empty room with the number of steps to its nearest gate, moving up, down, left or right and never through walls. A room that no gate can reach must stay INF.

Modify `rooms` in place; the function returns nothing.

Constraints:
- `1 <= m, n <= 250` for an `m x n` grid
- There may be many gates, or none
- Doing one search per room is too slow
