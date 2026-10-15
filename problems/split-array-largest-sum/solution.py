"""Split Array Largest Sum (#410, hard)

Approach: Binary search the answer between max(nums) and sum(nums); a cap is feasible if
    a greedy left-to-right split needs at most k pieces.
Tricks: Feasibility is monotonic in the cap, so search the answer space and let a greedy
    count do the checking.
Edge cases:
  - k = 1 (answer is the total sum)
  - k = n (answer is the largest element)
  - Zeros in the array
  - One huge element

Time O(n log(sum)), space O(1).
"""

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        # How many contiguous pieces are needed if no piece may sum above cap? Greedy:
        # keep extending the current piece, and start a new one only when forced to.
        def pieces_needed(cap: int) -> int:
            count, total = 1, 0
            for num in nums:
                if total + num > cap:
                    count += 1
                    total = 0
                total += num
            return count

        # The answer lies between the biggest single element (it must fit somewhere) and
        # the whole sum (k = 1). A larger cap never needs more pieces, so feasibility is
        # monotonic and we can binary search for the smallest cap that works.
        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:
                hi = mid  # mid works (fewer pieces can always be split further)
            else:
                lo = mid + 1
        return lo
