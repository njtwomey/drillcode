`board` is an `m x n` grid of the single-character strings `"X"` and `"O"`. A region is a group of orthogonally connected `"O"` cells. A region is surrounded if none of its cells lies on the border of the board.

Capture every surrounded region by turning all of its cells into `"X"`. Modify `board` in place; the function returns nothing. Regions touching the border keep their `"O"` cells.

Constraints:
- `1 <= m, n <= 200`
