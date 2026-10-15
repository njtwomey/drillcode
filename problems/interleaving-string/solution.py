"""Interleaving String (#97, medium)

Approach: Table where dp[i][j] says s3[:i+j] interleaves s1[:i] and s2[:j]; the last
    character must come from s1 or s2.
Tricks: Check len(s1) + len(s2) == len(s3) first, and try both sources for each
    character since equal letters make greedy matching fail.
Edge cases:
  - All strings empty
  - Length mismatch
  - Both strings start with the same letter

Time O(m·n), space O(m·n).
"""

class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        # The lengths must add up, otherwise no interleaving can exist.
        if m + n != len(s3):
            return False

        # dp[i][j] = True if s3[:i + j] is an interleaving of s1[:i] and s2[:j].
        # Base case: dp[0][0] = True (empty from empty). The first row and column are then
        # filled by the same rule, each using only one of the two strings.
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True

        # Loop order: dp[i][j] reads dp[i-1][j] and dp[i][j-1], so row-major order works.
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    continue
                # The last character of s3[:i + j] came from either s1 or s2. Both
                # options are tried because a greedy choice breaks when s1[i-1] == s2[j-1].
                ch = s3[i + j - 1]
                from_s1 = i > 0 and dp[i - 1][j] and s1[i - 1] == ch
                from_s2 = j > 0 and dp[i][j - 1] and s2[j - 1] == ch
                dp[i][j] = from_s1 or from_s2
        return dp[m][n]
