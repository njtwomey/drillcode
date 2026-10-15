"""Ransom Note (#383, easy)

Approach: Count magazine letters; decrement per note letter; fail if any count goes
    negative.
Tricks: A 26-element array beats a dictionary for lowercase-only input.
Edge cases:
  - Empty note (true)
  - Note longer than magazine

Time O(m + n), space O(1).
"""


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        counts = [0] * 26
        for ch in magazine:
            counts[ord(ch) - 97] += 1
        for ch in ransomNote:
            idx = ord(ch) - 97
            counts[idx] -= 1
            if counts[idx] < 0:
                return False
        return True
