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
        if len(word) > rows * cols:
            return False

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[i]:
                return False
            saved = board[r][c]
            board[r][c] = "#"
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
                     or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = saved
            return found

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
