"""Restore IP Addresses (#93, medium)

Approach: Backtrack over four segments of 1 to 3 digits, rejecting leading zeros and
    values above 255.
Tricks: Prune when the remaining digits cannot fit the remaining segments, and break at
    the first invalid length because longer pieces only get worse.
Edge cases:
  - Fewer than 4 or more than 12 digits
  - Leading zeros such as 010
  - Segment above 255

Time O(1), space O(1).
"""

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        result = []
        path = []  # dotted segments chosen so far

        def backtrack(start: int) -> None:
            parts_left = 4 - len(path)
            if parts_left == 0:
                if start == len(s):  # four segments and every digit consumed
                    result.append(".".join(path))
                return
            # Each remaining segment takes 1 to 3 digits, so the leftover length must
            # fit in that range or this branch can never finish.
            if not parts_left <= len(s) - start <= 3 * parts_left:
                return
            for end in range(start + 1, min(start + 3, len(s)) + 1):
                piece = s[start:end]
                # A longer piece only gets bigger, so stop at the first invalid one:
                # a leading zero ("0" alone is fine) or a value above 255.
                if (len(piece) > 1 and piece[0] == "0") or int(piece) > 255:
                    break
                path.append(piece)
                backtrack(end)
                path.pop()

        backtrack(0)
        return result
