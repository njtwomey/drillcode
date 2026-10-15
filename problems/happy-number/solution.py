"""Happy Number (#202, easy)

Approach: Iterate the digit-square-sum map with Floyd's slow and fast pointers; a
    meeting point other than 1 is a cycle.
Tricks: Values shrink to under 1000 after one step, so a cycle or 1 is guaranteed; a set
    of seen values is the simple alternative.
Edge cases:
  - n = 1
  - Numbers that fall into the 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 cycle
  - Largest 32-bit input

Time O(log n), space O(1).
"""

class Solution:
    def isHappy(self, n: int) -> bool:
        def next_value(x: int) -> int:
            # Sum of the squares of the decimal digits of x.
            total = 0
            while x:
                x, digit = divmod(x, 10)
                total += digit * digit
            return total

        # The sequence either reaches 1 (a fixed point) or falls into a cycle, because
        # the values stay small: even for a 10-digit n the next value is below 1000.
        # Floyd's tortoise and hare finds either ending without storing the sequence.
        slow = n
        fast = next_value(n)
        while fast != 1 and slow != fast:
            slow = next_value(slow)
            fast = next_value(next_value(fast))
        # Stopped on 1 means happy; stopped because the pointers met means a cycle.
        return fast == 1
