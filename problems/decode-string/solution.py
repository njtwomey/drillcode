"""Decode String (#394, medium)

Approach: Scan once; on "[" push the outer text and count then start fresh, on "]" pop
    and append the inner text repeated count times.
Tricks: Build counts digit by digit (num * 10 + digit) for multi-digit repeats, and
    reset num and curr every time a group opens.
Edge cases:
  - Multi-digit repeat count
  - Nested groups
  - Plain letters before, between and after groups
  - No brackets at all

Time O(output length), space O(output length).
"""

class Solution:
    def decodeString(self, s: str) -> str:
        # curr is the text built so far at the current nesting level, and num is the
        # repeat count being read for the group about to open.
        # On "[" we save the outer level (its text and the count) on the stack and start
        # fresh inside; on "]" we pop it and glue the repeated inner text back on.
        stack = []
        curr = ""
        num = 0
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)  # counts can have several digits
            elif ch == "[":
                stack.append((curr, num))
                curr, num = "", 0
            elif ch == "]":
                prev, count = stack.pop()
                curr = prev + curr * count
            else:
                curr += ch
        return curr
