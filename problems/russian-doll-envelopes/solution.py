"""Russian Doll Envelopes (#354, hard)

Approach: Sort by width ascending and height descending, then take the longest strictly
    increasing subsequence of heights with a tails array and bisect.
Tricks: The descending-height tie-break stops equal widths from chaining, and
    bisect_left keeps the chain strict.
Edge cases:
  - Identical envelopes
  - Equal widths with different heights
  - Equal heights with increasing widths

Time O(n log n), space O(n).
"""

from bisect import bisect_left


class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        # Sort by width ascending and, for equal widths, by height DESCENDING. Widths are
        # then non-decreasing, so only heights matter, and the descending tie-break stops
        # two envelopes of equal width from both entering a strictly increasing height
        # chain (the later, shorter one cannot extend the earlier, taller one).
        envelopes.sort(key=lambda e: (e[0], -e[1]))

        # Longest strictly increasing subsequence of heights, in O(n log n).
        # tails[k] = smallest possible last height of an increasing chain of length k + 1.
        # tails is always sorted, so bisect_left finds where a height belongs.
        tails = []
        for _, height in envelopes:
            # bisect_left (not bisect_right) keeps the chain strict: an equal height
            # replaces its twin instead of extending the chain.
            i = bisect_left(tails, height)
            if i == len(tails):
                tails.append(height)  # taller than every chain end: longest chain grows
            else:
                tails[i] = height  # a smaller end for chains of this length is never worse
        return len(tails)
