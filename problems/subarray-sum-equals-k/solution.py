"""Subarray Sum Equals K (#560, medium)

Approach: Running prefix sum with a map of prefix-sum counts; add the count of prefix -
    k at each step.
Tricks: Seed the map with {0: 1} and look up before inserting the current prefix, so k =
    0 does not count empty subarrays.
Edge cases:
  - Negative numbers and zeros (a sliding window fails)
  - k = 0 or negative k
  - Subarray starting at index 0

Time O(n), space O(n).
"""

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # count_of[p] = how many prefixes seen so far have sum p. The empty prefix (sum 0)
        # is seeded so subarrays starting at index 0 are counted.
        count_of = {0: 1}
        prefix = 0
        result = 0
        for num in nums:
            prefix += num
            # A subarray ending here sums to k exactly when an earlier prefix equals
            # prefix - k. Several earlier prefixes can share that sum (zeros, negatives),
            # and each one is a distinct subarray, so add the full tally.
            result += count_of.get(prefix - k, 0)
            # Record the current prefix only after the lookup, so k = 0 does not count
            # the empty subarray ending at this element.
            count_of[prefix] = count_of.get(prefix, 0) + 1
        return result
