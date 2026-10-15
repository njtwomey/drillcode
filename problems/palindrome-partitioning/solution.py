"""Palindrome Partitioning (#131, medium)

Approach: Backtrack on the start index, extending only with prefixes that are
    palindromes.
Tricks: Test the piece before recursing so dead branches are pruned; the answer is every
    path that reaches the end of the string.
Edge cases:
  - Single character
  - No palindrome longer than one character
  - Whole string is a palindrome

Time O(n * 2^n), space O(n).
"""

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result = []
        path = []

        # Choose the next piece s[start:end]; it must itself be a palindrome, which
        # prunes every branch that could never produce a valid partition.
        def backtrack(start: int) -> None:
            if start == len(s):
                result.append(path[:])
                return
            for end in range(start + 1, len(s) + 1):
                piece = s[start:end]
                if piece != piece[::-1]:
                    continue
                path.append(piece)
                backtrack(end)
                path.pop()

        backtrack(0)
        return result
