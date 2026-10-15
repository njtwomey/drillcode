"""Word Break (#139, medium)

Approach: dp[i] true if some j < i has dp[j] true and s[j:i] in the dictionary.
Tricks: Put words in a set; capping j at the longest word length prunes well.
Edge cases:
  - Words reusable
  - s shorter than every word
  - a word that is a prefix of another

Time O(n · L), space O(n).
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
