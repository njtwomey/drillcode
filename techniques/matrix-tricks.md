---
title: Matrix manipulation
area: Matrices
topics: [Matrix]
problems:
  - rotate-image
  - spiral-matrix
  - set-matrix-zeroes
  - search-a-2d-matrix
  - valid-sudoku
related: [grid-traversal, binary-search-shapes]
---
## Reach for it when
- The task is "in place" on a grid, with O(1) extra space.
- It says rotate, transpose, or spiral.
- Rows and columns must be marked or cleared together (set zeroes).
- A sorted matrix is searched as if it were one list.
- Each cell belongs to several groups at once (row, column, 3x3 box).

## Setup
- `rows, cols = len(matrix), len(matrix[0])`. Name them once and use them for every bound.
- For spiral: `top, bottom, left, right`. Invariant: they bound the rectangle not yet visited.
- For set zeroes: `first_row`, `first_col` flags, computed before any marking. Invariant: the first row and column hold markers for the inner cells until the final step.
- For a flat search: `lo, hi = 0, rows * cols - 1`, and `r, c = divmod(mid, cols)`.
- For sudoku: `rows`, `cols`, `boxes`, each a list of 9 sets. Invariant: each holds the digits seen in that unit.

## Template
In-place clockwise rotation: transpose, then reverse each row.

```python
def rotate_clockwise(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
```

## What it removes
- A second matrix for rotation. Transpose plus mirror equals a quarter turn, done by swaps.
- Extra row and column sets in set zeroes. The first row and column serve as the marker store.
- A nested binary search in `search-a-2d-matrix`. Index arithmetic turns the matrix into one sorted array without building it.
- Direction bookkeeping in spiral. Four shrinking boundaries replace a direction vector and a visited grid.

## Pitfalls
- Transposing the full square. Swapping `(i, j)` for every `j` swaps each pair twice and returns the original. Start `j` at `i + 1`.
- Counter-clockwise is transpose then reverse each column (or reverse the rows first, then transpose). Reversing rows gives the wrong turn direction.
- Spiral visiting cells twice. After the top and right edges, re-check `top <= bottom` before the bottom edge and `left <= right` before the left edge. A single row such as `[[1, 2, 3]]` otherwise returns `[1, 2, 3, 3, 2, 1]`.
- Zeroing the marker row or column before reading it. Symptom: the whole matrix becomes zeros. Do the inner cells first and the first row and column last, from the saved flags.
- Using `matrix[0][0]` as both row and column marker. Keep a separate flag for the first column.
- Box index: `(r // 3) * 3 + c // 3`. Writing `r // 3 + c // 3` collides boxes.

## Variants
- Rotate: `rotate-image`.
- Boundary peeling: `spiral-matrix`.
- Marker borders: `set-matrix-zeroes`.
- Flat index to 2D: `search-a-2d-matrix` with `mid // cols` and `mid % cols`.
- Unit index: `valid-sudoku` maps a cell to its row, column and box sets.

## Worked example
Problem: `rotate-image`

Transpose across the main diagonal, then mirror each row.

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        # Step 1: transpose (reflect over the main diagonal), so (i, j) -> (j, i).
        # Starting j at i + 1 visits each pair once; swapping the whole square would
        # undo itself, and the diagonal does not move.
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Step 2: reversing each row mirrors left to right. Transpose plus mirror
        # equals a 90 degree clockwise turn, done in place with no second matrix.
        for row in matrix:
            row.reverse()
```

The first double loop is the transpose, with `j` starting at `i + 1`. The second loop reverses each `row`. `n` is the size, and nothing else is allocated.
