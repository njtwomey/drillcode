"""Valid Sudoku (#36, medium)

Approach: Sets per row, column and 3x3 box; fail on any repeat.
Tricks: Box index is (r // 3) * 3 + c // 3.
Edge cases:
  - Empty board is valid
  - Only placed digits are checked, not solvability

Time O(1), space O(1).
"""


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                d = board[r][c]
                if d == ".":
                    continue
                b = (r // 3) * 3 + c // 3
                if d in rows[r] or d in cols[c] or d in boxes[b]:
                    return False
                rows[r].add(d)
                cols[c].add(d)
                boxes[b].add(d)
        return True
