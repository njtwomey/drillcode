"""Count magazine letters in a 26-slot array; spend one per ransom note letter.
Fail as soon as a count would go negative.

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
