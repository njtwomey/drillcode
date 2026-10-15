"""Find All Numbers Disappeared in an Array (#448, easy)

Approach: Use the array as its own seen-set by negating nums[v - 1] for each value v,
    then report the slots still positive.
Tricks: Read values with abs() since earlier steps may have negated them, and set -abs()
    so duplicates do not flip the sign back.
Edge cases:
  - Duplicates hitting an already marked slot
  - Permutation (nothing missing)
  - All values equal

Time O(n), space O(1).
"""

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        # Every value is in 1..n, so value v can mark "v is present" by flipping the sign
        # of nums[v - 1]. The array itself becomes the seen-set, using no extra space.
        for num in nums:
            # abs() because an earlier step may already have negated this element, and
            # setting -abs() (not -x) keeps repeated marks from flipping the sign back.
            index = abs(num) - 1
            nums[index] = -abs(nums[index])
        # A slot still positive was never marked, so index + 1 never appeared.
        return [i + 1 for i, num in enumerate(nums) if num > 0]
