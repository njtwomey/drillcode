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
        stack = []
        for token in tokens:
            if token in ("+", "-", "*", "/"):
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))
            else:
                stack.append(int(token))
        return stack[0]
