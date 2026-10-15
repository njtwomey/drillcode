"""Permutation in String (#567, medium)

Approach: Slide a window of len(s1) over s2 keeping 26 letter counts and compare to the
    counts of s1.
Tricks: Fixed window, so add the new right char and remove the char that just left;
    return False early if s1 is longer.
Edge cases:
  - s1 longer than s2
  - Match at the very end
  - Right letters but wrong counts

Time O(n), space O(1).
"""

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m = len(s1)
        if m > len(s2):
            return False
        # A permutation of s1 is any substring of s2 with the same letter counts and
        # length m. Slide a fixed-size window and compare 26-slot count arrays.
        need = [0] * 26
        window = [0] * 26
        for ch in s1:
            need[ord(ch) - 97] += 1
        for i, ch in enumerate(s2):
            window[ord(ch) - 97] += 1
            # Once the window is longer than m, drop its oldest character.
            if i >= m:
                window[ord(s2[i - m]) - 97] -= 1
            if window == need:
                return True
        return False
