"""Decode Ways (#91, medium)

Approach: dp[i] = dp[i-1] if s[i] != '0', plus dp[i-2] if the two-character value is in
    10..26.
Tricks: '0' can only attach to a preceding 1 or 2; it contributes nothing on its own.
Edge cases:
  - Leading zero (0 ways)
  - "10"
  - "20"
  - "27"
  - "100"

Time O(n), space O(1).
"""


class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 0, 1  # ways for prefixes of length i-2 and i-1; empty prefix has 1 way
        for i in range(1, len(s) + 1):
            cur = 0
            # One-digit decode: any digit but '0' stands alone as a letter.
            if s[i - 1] != "0":
                cur += prev1
            # Two-digit decode: 10..26 only. This rejects '0X' (leading zero) and 27+, and
            # lets '10'/'20' work, since their '0' is not usable on its own.
            if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
                cur += prev2
            # Slide the window; only the last two counts are ever needed.
            prev2, prev1 = prev1, cur
        return prev1
