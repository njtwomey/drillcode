"""Regular Expression Matching (#10, hard)

Approach: 2D DP where dp[i][j] means s[:i] matches p[:j]; a star either drops its item
    (zero copies) or consumes one more matching character.
Tricks: For the star's one-more case look at dp[i-1][j], same column, so the item can
    repeat; fill row 0 too so patterns like a*b* match the empty prefix.
Edge cases:
  - Star matching zero characters
  - Dot star swallowing everything or backing off for a tail
  - String longer than the pattern
  - Exponential backtracking pattern a*a*a*b

Time O(m * n), space O(m * n).
"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        # dp[i][j] = s[:i] matches p[:j]  (whole prefixes, not just a suffix of them).
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True  # empty string matches empty pattern
        # Row i = 0 is filled by the same loop: "a*b*" can match the empty string
        # because each starred item can take zero copies.
        for i in range(m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == "*":
                    # The star applies to p[j-2] (a valid pattern never starts with
                    # '*'). Case 1: zero copies, drop the two-character item "x*".
                    dp[i][j] = dp[i][j - 2]
                    # Case 2: one more copy. p[j-2] must match the last character of
                    # s[:i]; then s[:i-1] has to match the same p[:j], since the star
                    # may still absorb more. Staying on column j is what lets it repeat.
                    if i > 0 and (p[j - 2] == "." or p[j - 2] == s[i - 1]):
                        dp[i][j] = dp[i][j] or dp[i - 1][j]
                elif i > 0 and (p[j - 1] == "." or p[j - 1] == s[i - 1]):
                    # Plain character or '.': consume one from each side.
                    dp[i][j] = dp[i - 1][j - 1]
        return dp[m][n]
