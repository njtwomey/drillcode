"""Range Sum Query - Immutable (#303, easy)

Approach: Precompute a prefix-sum array once; each query is a subtraction of two
    prefixes.
Tricks: Prefix array has length n + 1 with a leading 0, so a range starting at index 0
    needs no special case.
Edge cases:
  - Range covering a single index
  - Range starting at index 0
  - Negative values

Time O(n) build, O(1) per query, space O(n).
"""

class NumArray:
    def __init__(self, nums: List[int]):
        # prefix[i] = sum of nums[:i]. The leading 0 means a range starting at index 0
        # needs no special case.
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        # Subtracting two prefixes cancels everything before left, leaving nums[left..right].
        return self.prefix[right + 1] - self.prefix[left]
