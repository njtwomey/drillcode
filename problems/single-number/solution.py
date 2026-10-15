"""Single Number (#136, easy)

Approach: XOR every element; pairs cancel and the single value remains.
Tricks: x ^ x is 0 and x ^ 0 is x, and XOR is order independent.
Edge cases:
  - Single element
  - Negative numbers
  - The single value is 0

Time O(n), space O(1).
"""

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # XOR is commutative and associative, x ^ x == 0 and x ^ 0 == x. Folding the
        # whole array cancels every pair (in any order) and leaves the lone element.
        result = 0
        for num in nums:
            result ^= num
        return result
