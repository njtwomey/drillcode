"""Basic Calculator (#224, hard)

Approach: One pass keeping a running result and sign, pushing (result, sign) on each
    open parenthesis and folding it back on the close.
Tricks: With only + and - a bracket is just a sign on its subtotal, so unary minus needs
    no special case since the committed number is 0.
Edge cases:
  - Unary minus at the start or right after a parenthesis
  - Nested and redundant parentheses
  - Spaces and multi-digit numbers

Time O(n), space O(n).
"""

class Solution:
    def calculate(self, s: str) -> int:
        # Only + and - exist, so a parenthesis is just a sign applied to a subtotal:
        # a - (b + c) = a - b - c. We never need operator precedence, only to save
        # (running total, sign in front of the bracket) when a bracket opens.
        result = 0  # total of the current bracket level, excluding the pending number
        sign = 1  # sign for the number being read
        num = 0
        stack = []
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch in "+-":
                result += sign * num  # commit the finished number
                num = 0
                sign = 1 if ch == "+" else -1
                # A leading "-" (start of string or right after "(") works too: the
                # number committed above is 0.
            elif ch == "(":
                # Park the outer total and the sign in front of this bracket, then
                # start a fresh sub-expression.
                stack.append(result)
                stack.append(sign)
                result, sign = 0, 1
            elif ch == ")":
                result += sign * num  # finish the bracket's subtotal
                num = 0
                result *= stack.pop()  # apply the sign that preceded "("
                result += stack.pop()  # add back the outer total
            # spaces are ignored
        return result + sign * num
