"""Implement Queue using Stacks (#232, easy)

Approach: Two stacks: push onto the in-stack, pop from the out-stack, transferring only
    when the out-stack is empty.
Tricks: Each element moves across at most once, so operations are amortised O(1).
Edge cases:
  - Pop or peek when the out-stack is empty but the in-stack is not

Time O(1) amortised, space O(n).
"""


class MyQueue:
    def __init__(self):
        # in_stack receives pushes (newest on top); out_stack serves pops (oldest on top).
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _shift(self) -> None:
        # Only refill when out_stack is empty. Moving earlier would put newer items under
        # older ones and break FIFO order. Popping in_stack into out_stack reverses it,
        # so the oldest element ends up on top. Each element moves once, hence amortised O(1).
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._shift()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._shift()
        return self.out_stack[-1]

    def empty(self) -> bool:
        # Elements may sit in either stack, so both must be empty.
        return not self.in_stack and not self.out_stack
