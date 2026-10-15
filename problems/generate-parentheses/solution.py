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
        path = []

        def dfs(opens, closes):
            if len(path) == 2 * n:
                result.append("".join(path))
                return
            if opens < n:
                path.append("(")
                dfs(opens + 1, closes)
                path.pop()
            if closes < opens:
                path.append(")")
                dfs(opens, closes + 1)
                path.pop()

        dfs(0, 0)
        return result
