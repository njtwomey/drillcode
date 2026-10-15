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
        words = set(wordDict)  # O(1) average membership instead of scanning a list
        longest = max(len(w) for w in words)
        # dp[i] means: the prefix s[:i] can be split into dictionary words.
        dp = [False] * (len(s) + 1)
        dp[0] = True  # empty prefix is trivially breakable; seeds every later state
        for i in range(1, len(s) + 1):
            # Try every last word s[j:i]. No word is longer than `longest`, so earlier j
            # can't match; this caps the inner loop at L and gives O(n * L) splits.
            for j in range(max(0, i - longest), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break  # one valid split is enough
        return dp[len(s)]
