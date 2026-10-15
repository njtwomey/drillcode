"""Find All Anagrams in a String (#438, medium)

Approach: Fixed window of len(p) over s with 26 letter counts; record the start index
    whenever the counts equal those of p.
Tricks: Only compare once the window is full, and the start index is i - len(p) + 1.
Edge cases:
  - p longer than s
  - Overlapping matches
  - Repeated letters

Time O(n), space O(1).
"""

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        m = len(p)
        result = []
        if m > len(s):
            return result
        # Same fixed-window idea as Permutation in String, but record every start index
        # instead of stopping at the first hit.
        need = [0] * 26
        window = [0] * 26
        for ch in p:
            need[ord(ch) - 97] += 1
        for i, ch in enumerate(s):
            window[ord(ch) - 97] += 1
            if i >= m:
                window[ord(s[i - m]) - 97] -= 1  # the char that slid out on the left
            # The window ends at i, so it starts at i - m + 1 (only valid once it is full).
            if i >= m - 1 and window == need:
                result.append(i - m + 1)
        return result
