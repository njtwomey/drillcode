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
        # Cheap early exit: a longer note can never be built from a shorter magazine.
        if len(ransomNote) > len(magazine):
            return False
        # Fixed 26 slots (lowercase only) keeps space O(1) and avoids hashing.
        counts = [0] * 26
        for ch in magazine:
            counts[ord(ch) - 97] += 1
        # Spend one magazine letter per note letter.
        for ch in ransomNote:
            idx = ord(ch) - 97
            counts[idx] -= 1
            # Below zero means the note needs more of this letter than we have.
            if counts[idx] < 0:
                return False
        return True
