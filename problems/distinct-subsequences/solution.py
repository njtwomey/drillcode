"""Distinct Subsequences (#115, hard)

Approach: Table where dp[i][j] counts ways s[:i] spells t[:j]; skip s[i-1] always, and
    also use it when it equals t[j-1].
Tricks: Seed dp[i][0] = 1 for every i, since the empty target is formed by choosing
    nothing; count by positions, not by distinct strings.
Edge cases:
  - Target longer than source (0)
  - Many repeated characters, so counts are binomial
  - Characters present but in the wrong order

Time O(m·n), space O(m·n).
"""

class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        # dp[i][j] = number of ways to pick a subsequence of s[:i] that spells t[:j].
        # Base cases: dp[i][0] = 1 for every i (the empty target can be formed by choosing
        # nothing), and dp[0][j] = 0 for j > 0 (an empty source cannot spell anything).
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = 1

        # Loop order: row i reads only row i-1, so row-major order works.
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Every way that never uses s[i-1] still counts.
                dp[i][j] = dp[i - 1][j]
                # If s[i-1] matches the last wanted character, we may also spend it there,
                # leaving the other characters to spell t[:j-1] from s[:i-1].
                if s[i - 1] == t[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]
        return dp[m][n]
