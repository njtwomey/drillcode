"""DFS building the string, adding '(' while opens < n and ')' while closes < opens.

The closes < opens rule alone keeps every prefix valid, so no stack is needed.
Time O(4^n / sqrt(n)), space O(n) excluding the output.
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
