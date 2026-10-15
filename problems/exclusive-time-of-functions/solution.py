"""Exclusive Time of Functions (#636, medium)

Approach: Stack of (id, start); on end add the inclusive span to that function and
    subtract it from the caller below.
Tricks: End timestamps are inclusive so a span is end - start + 1; subtracting callee
    spans from the caller handles recursion and nesting.
Edge cases:
  - A function calling itself recursively
  - A call that starts and ends in the same unit
  - A function that never appears in the logs

Time O(L), space O(L).
"""

class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        result = [0] * n
        stack = []  # (function id, start time) of every call still running
        for log in logs:
            fid, kind, stamp = log.split(":")
            fid, stamp = int(fid), int(stamp)
            if kind == "start":
                stack.append((fid, stamp))
            else:
                # An end timestamp is inclusive (the function runs during that whole
                # unit), hence the + 1. The span includes time spent in nested calls.
                _, start = stack.pop()
                span = stamp - start + 1
                result[fid] += span
                # The caller was not running during the span, so take it back out of
                # the caller's total. Recursion works because each call is its own
                # stack entry, even when the id is the same.
                if stack:
                    result[stack[-1][0]] -= span
        return result
