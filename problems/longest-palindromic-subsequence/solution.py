"""Longest Palindromic Subsequence (#516, medium)

Approach: Interval table where dp[i][j] is the best palindromic subsequence of s[i..j];
    equal ends add 2 to the inside, otherwise drop one end.
Tricks: Fill i from the end and j from i+1 so the inner and shorter ranges are already
    known; a subsequence is not a substring.
Edge cases:
  - Single character
  - All characters distinct (answer 1)
  - Whole string already a palindrome

Time O(n²), space O(n²).
"""

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        # dp[i][j] = length of the longest palindromic subsequence of s[i..j] inclusive.
        # Base cases: dp[i][i] = 1 (a single character), and an empty range (j < i) is 0,
        # which the zero-initialised table already gives us.
        dp = [[0] * n for _ in range(n)]

        # Loop order: dp[i][j] reads dp[i+1][j-1], dp[i+1][j] and dp[i][j-1]. Every one of
        # those has a larger i or a smaller j, so i runs backwards and j runs forwards.
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    # Matching ends wrap whatever the best palindrome inside is.
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    # At most one end can be used: drop either the left or the right.
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return dp[0][n - 1] if n else 0
