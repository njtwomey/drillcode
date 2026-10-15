"""Longest Common Subsequence (#1143, medium)

Approach: 2D DP: dp[i][j] = dp[i-1][j-1] + 1 on a match, else max(dp[i-1][j],
    dp[i][j-1]).
Tricks: Subsequence, not substring, so the else branch carries values forward.
Edge cases:
  - One string empty
  - No characters in common

Time O(m · n), space O(m · n).
"""


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        # dp[i][j] = LCS length of text1[:i] and text2[:j]. The extra row and column of
        # zeros are the empty-prefix base cases, so no index checks are needed below.
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # i - 1 / j - 1 because dp is shifted by one relative to the strings.
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1  # matching chars extend the best so far
                else:
                    # No match: drop the last char of one string or the other, keep the better.
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
