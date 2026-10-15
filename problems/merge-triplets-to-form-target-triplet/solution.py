"""Merge Triplets to Form Target Triplet (#1899, medium)

Approach: Skip every triplet with a coordinate above the target, then check each target
    coordinate is matched by some remaining triplet.
Tricks: Max never decreases, so one oversized coordinate poisons a triplet; a matching
    value inside a discarded triplet does not count.
Edge cases:
  - Only triplet exceeds the target
  - Target value present only in a discarded triplet
  - Each coordinate supplied by a different triplet

Time O(n), space O(1).
"""

class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        # Merging takes the coordinate-wise max, so a value can never come back down.
        # Any triplet with a coordinate above the target would ruin that slot forever:
        # it is never safe to use, so ignore it completely.
        # For the rest, merging all of them is harmless (each stays <= target), so the
        # only question is whether every target coordinate is hit exactly by some usable
        # triplet.
        found = [False, False, False]
        for triplet in triplets:
            if triplet[0] > target[0] or triplet[1] > target[1] or triplet[2] > target[2]:
                continue
            for i in range(3):
                if triplet[i] == target[i]:
                    found[i] = True
        return all(found)
