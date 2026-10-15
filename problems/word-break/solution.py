"""dp[i] is true if some j < i has dp[j] true and s[j:i] in the word set.

Only j within the longest word length of i are tried. Words may be reused.
Time O(n * L) substring checks (L = longest word), space O(n).
"""


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        longest = max(len(w) for w in words)
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(max(0, i - longest), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[len(s)]
