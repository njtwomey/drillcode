"""Longest Common Prefix (#14, easy)

Approach: Scan column by column across all strings and stop at the first string that is
    too short or differs from the first.
Tricks: Check the index against each string's length before comparing, so a short string
    ends the scan safely.
Edge cases:
  - No common prefix
  - A single string
  - Identical strings
  - An empty string in the array

Time O(S), space O(1).
"""

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # Vertical scan: compare column i across all strings, and stop at the first
        # column where any string is too short or disagrees with the first one.
        first = strs[0]
        for i, c in enumerate(first):
            for s in strs:
                if i == len(s) or s[i] != c:
                    return first[:i]
        return first  # the first string is a prefix of every other string
