"""Bitwise AND of Numbers Range (#201, medium)

Approach: Shift left and right together until they are equal, then shift the common
    prefix back.
Tricks: Every bit below the first differing bit is 0 in some number of the range, so
    only the common prefix survives.
Edge cases:
  - left equals right
  - Range starting at 0
  - Range up to 2^31 - 1

Time O(log max), space O(1).
"""

class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        # Counting up from left to right flips every bit below the highest bit where
        # the two differ (somewhere in the range each of those bits is 0). Only the
        # common binary prefix of left and right survives the AND.
        # Shift both right until they agree, remembering how far we went.
        shift = 0
        while left != right:
            left >>= 1
            right >>= 1
            shift += 1
        # Restore the prefix to its original position; the low bits are all zero.
        return left << shift
