Given an `m x n` grid `matrix` whose cells are the strings `"0"` and `"1"`, find the largest square made up entirely of `"1"` cells and return its area (side length squared). Return 0 if the grid has no `"1"`. The square must be axis-aligned and contiguous.

Constraints:
- `1 <= m, n <= 300`
- Each cell is the character string `"0"` or `"1"`, not an integer
- Checking every possible square from scratch is too slow; aim for O(m*n)
