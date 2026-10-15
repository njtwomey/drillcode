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
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _shift(self) -> None:
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
        return not self.in_stack and not self.out_stack
