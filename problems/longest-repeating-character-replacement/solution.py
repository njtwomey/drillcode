"""Longest Repeating Character Replacement (#424, medium)

Approach: Window valid while length - maxCount <= k; shrink from the left when it is not.
Tricks: maxCount need not be decremented when shrinking; a stale value never yields a
    wrong answer.
Edge cases:
  - k = 0
  - k >= length (whole string)
  - Single character

Time O(n), space O(1).
"""


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Window [left, right] is valid if we can make it one letter with <= k edits:
        # edits needed = window length - count of its most frequent letter.
        counts = {}
        max_count = 0
        left = 0
        best = 0
        for right, ch in enumerate(s):
            counts[ch] = counts.get(ch, 0) + 1
            # max_count is never lowered. The answer only grows when max_count grows, so a
            # stale (too high) value can only keep the window the same size, never inflate it.
            max_count = max(max_count, counts[ch])
            # Invalid: slide the window by shrinking one step, so its size never decreases.
            if (right - left + 1) - max_count > k:
                counts[s[left]] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
