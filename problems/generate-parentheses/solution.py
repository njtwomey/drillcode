"""Generate Parentheses (#22, medium)

Approach: DFS adding '(' while opens < n and ')' while closes < opens.
Tricks: The closes < opens rule alone guarantees validity; no stack needed.
Edge cases:
  - n = 1

Time O(4^n / √n), space O(n).
"""


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        # path is the string built so far; we add and undo characters (backtracking).
        path = []

        def dfs(opens, closes):
            # Full length reached. The two rules below guarantee it is balanced.
            if len(path) == 2 * n:
                result.append("".join(path))
                return
            # May open while we have opens left to use.
            if opens < n:
                path.append("(")
                dfs(opens + 1, closes)
                path.pop()
            # May close only if an open is unmatched; this stops prefixes like ")(".
            # Every branch leads to a valid answer, so no work is wasted on dead ends.
            if closes < opens:
                path.append(")")
                dfs(opens, closes + 1)
                path.pop()

        dfs(0, 0)
        return result
