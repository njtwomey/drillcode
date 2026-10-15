"""Remove K Digits (#402, medium)

Approach: Greedily pop the previous digit while it is larger than the incoming one and
    removals remain, then trim leftovers from the end.
Tricks: After the loop any remaining k is removed from the tail of the non-decreasing
    stack, and the result needs lstrip("0") or "0".
Edge cases:
  - k equals len(num) (result "0")
  - Leading zeros after removal
  - Already non-decreasing digits
  - Digit that is removed from the middle of a run of equal digits

Time O(n), space O(n).
"""

class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        # Greedy: a smaller digit in a more significant position always wins. So whenever
        # the incoming digit is smaller than the one before it, drop that earlier digit.
        # The stack stays non-decreasing, which is the smallest possible prefix.
        stack = []
        for digit in num:
            while k and stack and stack[-1] > digit:
                stack.pop()
                k -= 1
            stack.append(digit)
        # Still owe removals: the stack is non-decreasing, so the largest digits are at
        # the end. Trim from there (k is 0 here when nothing is left to remove).
        if k:
            stack = stack[:-k]
        # Leading zeros do not count, and removing everything must read as "0".
        return "".join(stack).lstrip("0") or "0"
