"""Partition Labels (#763, medium)

Approach: Record each letter's last index, then extend the current part's end and cut
    when the index reaches it.
Tricks: Cut as soon as the scan index equals the farthest last occurrence seen so far.
Edge cases:
  - All letters distinct
  - One letter repeated across the whole string
  - Single character

Time O(n), space O(1).
"""

class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        # last[c] is the final index of letter c, so a part that contains c must reach
        # at least that far.
        last = {c: i for i, c in enumerate(s)}
        result = []
        start = 0  # first index of the current part
        end = 0  # farthest index the current part is forced to reach
        # Greedy: cut as soon as the forced end is reached. Cutting earlier is
        # impossible (some letter would straddle the cut), and cutting later would only
        # merge two parts that could have been separate, giving fewer parts.
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                result.append(end - start + 1)
                start = i + 1
        return result
