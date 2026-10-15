"""Remember every value seen; a repeat means a cycle.

Time O(log n) per step with a bounded number of steps, space O(number of distinct values).
"""


class Solution:
    def isHappy(self, n: int) -> bool:
        def next_value(x: int) -> int:
            total = 0
            while x:
                x, digit = divmod(x, 10)
                total += digit * digit
            return total

        seen = set()
        # Reaching 1 ends the loop happily; revisiting any value means we are cycling.
        while n != 1 and n not in seen:
            seen.add(n)
            n = next_value(n)
        return n == 1
