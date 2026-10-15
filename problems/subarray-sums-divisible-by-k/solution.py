"""Subarray Sums Divisible by K (#974, medium)

Approach: Count prefix sums by remainder mod k; each pair of equal remainders is one
    divisible subarray.
Tricks: Seed remainder 0 with a count of 1; Python's % keeps negative prefixes in [0,
    k), other languages need a fix-up.
Edge cases:
  - Negative numbers (negative prefix remainders)
  - Zeros
  - Subarray starting at index 0

Time O(n), space O(k).
"""

class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        # A subarray sum is divisible by k exactly when the two prefix sums bounding it
        # have the same remainder mod k. So count pairs of equal remainders.
        # The empty prefix has remainder 0, which covers subarrays starting at index 0.
        count_of = {0: 1}
        prefix = 0
        result = 0
        for num in nums:
            # Python's % returns a value in [0, k) even for negative prefixes, so -1 and
            # k - 1 land in the same bucket as they should. (C++/Java would need a fix-up.)
            prefix = (prefix + num) % k
            # Each earlier prefix with this remainder forms one valid subarray with us.
            result += count_of.get(prefix, 0)
            count_of[prefix] = count_of.get(prefix, 0) + 1
        return result
