"""Evaluate Reverse Polish Notation (#150, medium)

Approach: Push numbers; on an operator, pop two and push the result.
Tricks: Operand order matters for - and /; division truncates toward zero (int(a / b) in
    Python).
Edge cases:
  - Negative numbers
  - Division such as 6 / -132
  - Single token

Time O(n), space O(n).
"""


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        # Operands wait on the stack until an operator consumes the two most recent ones.
        stack = []
        for token in tokens:
            if token in ("+", "-", "*", "/"):
                # b is popped first because it was pushed last (the right operand).
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                else:
                    # int() truncates toward zero as the problem requires; // would floor
                    # negatives (-7 // 2 is -4, but the answer is -3).
                    stack.append(int(a / b))
            else:
                stack.append(int(token))
        # A valid expression leaves exactly one value: the result.
        return stack[0]
