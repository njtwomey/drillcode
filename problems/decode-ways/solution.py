"""dp[i] = dp[i-1] if s[i-1] != '0', plus dp[i-2] if the two-digit value is in 10..26.

Only the last two dp values are kept.
Time O(n), space O(1).
"""


class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 0, 1  # ways for prefixes of length i-2 and i-1; empty prefix has 1 way
        for i in range(1, len(s) + 1):
            cur = 0
            if s[i - 1] != "0":
                cur += prev1
            if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
                cur += prev2
            prev2, prev1 = prev1, cur
        return prev1
