"""Basic Calculator II (#227, medium)

Approach: One pass with a stack of terms; push signed numbers for + and -, apply * and /
    immediately to the top, then sum the stack.
Tricks: Apply the previous operator when you reach the next one, add a sentinel to flush
    the last number, and truncate division toward zero rather than flooring.
Edge cases:
  - Spaces anywhere including the ends
  - Multi-digit numbers
  - Division of a negative term (truncate toward zero)
  - Expression that is a single number

Time O(n), space O(n).
"""

class Solution:
    def calculate(self, s: str) -> int:
        # Evaluate left to right with a stack of terms to be summed at the end. "*" and
        # "/" bind tighter, so they are applied immediately to the latest term, while
        # "+" and "-" just push a (signed) new term.
        # op is the operator that came BEFORE num, which is why it is applied when we
        # reach the next operator. The sentinel "+" at the end flushes the last number.
        stack = []
        num = 0
        op = "+"
        for ch in s + "+":
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == " ":
                continue
            else:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    # Truncate toward zero: floor division would round negatives down.
                    top = stack.pop()
                    quotient = abs(top) // num
                    stack.append(quotient if top >= 0 else -quotient)
                op = ch
                num = 0
        return sum(stack)
