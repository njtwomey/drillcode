"""Letter Combinations of a Phone Number (#17, medium)

Approach: DFS over the digits, appending each mapped letter.
Tricks: A digit-to-letters table handles 7 and 9 having four letters.
Edge cases:
  - Empty input returns an empty list, not a list containing an empty string

Time O(4^n · n), space O(n).
"""


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        # Without this, DFS would return [""] for empty input; LeetCode expects [].
        if not digits:
            return []
        mapping = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }
        # Digits 7 and 9 map to four letters, so a table is simpler than arithmetic.
        result = []
        path = []

        # Backtracking: i is the digit we are choosing a letter for. path holds the
        # letters chosen for digits[:i]; each leaf of the tree is one full combination.
        def dfs(i):
            if i == len(digits):
                result.append("".join(path))
                return
            for ch in mapping[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()  # undo the choice so the next letter starts from the same prefix

        dfs(0)
        return result
