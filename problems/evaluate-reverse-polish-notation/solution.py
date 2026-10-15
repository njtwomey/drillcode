"""Push numbers on a stack; on an operator pop two, apply, push the result.

Pop the right operand first (matters for - and /); division truncates toward zero.
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
