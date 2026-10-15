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
        self.stack = []

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
