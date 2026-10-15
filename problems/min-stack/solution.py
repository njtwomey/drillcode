"""Min Stack (#155, medium)

Approach: Store (value, min so far) per entry, or keep a parallel min stack.
Tricks: Push to the min stack only when the value is <= the current min, and pop it in
    step.
Edge cases:
  - Duplicate minimums
  - Pop that removes the current min

Time O(1) per operation, space O(n).
"""


class MinStack:
    def __init__(self):
        # Each entry stores (value, min of the stack up to and including it), so the
        # min is restored automatically on pop without searching. All ops are O(1).
        self.stack = []

    def push(self, val: int) -> None:
        # Empty stack: val is the min. Otherwise compare with the min below it.
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
