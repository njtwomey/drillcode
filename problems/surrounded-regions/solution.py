"""Surrounded Regions (#130, medium)

Approach: Flood-fill from every border 'O' to mark the safe ones, then flip the
    remaining 'O' to 'X' and restore the marks.
Tricks: Search from the border inwards instead of testing each region; the safe marker
    doubles as the visited flag.
Edge cases:
  - Single cell
  - Single row or column, where everything is on the border
  - Diagonal contact with the border does not connect

Time O(m * n), space O(m * n).
"""

# Judge notes:
# Do not return anything: modify board in place instead.


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        # Think backwards: an 'O' survives only if it connects to the border. So mark
        # every border-connected 'O' as safe, then flip whatever is left.
        stack = [(r, c) for r in range(rows) for c in range(cols)
                 if (r in (0, rows - 1) or c in (0, cols - 1)) and board[r][c] == "O"]
        while stack:
            r, c = stack.pop()
            if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != "O":
                continue
            board[r][c] = "S"  # the marker doubles as the visited flag
            stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
        # Final sweep: remaining 'O' cells were enclosed; 'S' cells go back to 'O'.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"
