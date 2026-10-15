"""DFS over the digits, appending each letter mapped to the current digit.

Empty input returns [] rather than [""].
Time O(4^n * n), space O(n) excluding the output.
"""


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        mapping = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }
        result = []
        path = []

        def dfs(i):
            if i == len(digits):
                result.append("".join(path))
                return
            for ch in mapping[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()

        dfs(0)
        return result
