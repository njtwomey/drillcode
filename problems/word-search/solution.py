"""Word Search (#79, medium)

Approach: DFS from each cell matching the next character, marking cells visited and
    restoring on return.
Tricks: Mark the cell in the grid itself (e.g. '#') and restore it after recursing,
    instead of a visited set.
Edge cases:
  - Word longer than the grid has cells
  - 1x1 grid
  - Repeated letters in the word

Time O(m·n·3^L), space O(L).
"""


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        # Cheap prune: a path can't reuse cells, so the word can't be longer than the grid.
        if len(word) > rows * cols:
            return False

        # dfs(r, c, i): can word[i:] be matched starting at (r, c)?
        def dfs(r, c, i):
            if i == len(word):
                return True  # every character matched
            # Bounds check first, then the character check. A "#" cell (on our current
            # path) never equals a letter, so it is rejected here for free.
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
                return False
            # Mark the cell as used on this path, in place, so no visited set is needed.
            saved = board[r][c]
            board[r][c] = "#"
            # `or` short-circuits: stop exploring as soon as one direction succeeds.
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
                     or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            # Backtrack: restore so other paths (other start cells) can use this cell.
            board[r][c] = saved
            return found

        # Try every cell as a start. Each DFS branches at most 3 ways after the first
        # step (the cell we came from is marked), hence 3^L.
        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
