You are given a `triangle` as a list of rows, where row `i` has `i + 1` integers. Find the minimum sum of a path from the top row to the bottom row. From the cell at index `j` in a row you may step to either index `j` or index `j + 1` in the next row. Return the smallest total of the values visited.

Constraints:
- `1 <= len(triangle) <= 200`
- `-10^4 <= triangle[i][j] <= 10^4`
- Trying every path takes 2^n time; aim for O(n^2) time in the number of cells, ideally with O(n) extra space
