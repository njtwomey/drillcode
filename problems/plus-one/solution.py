"""Plus One (#66, easy)

Approach: Scan from the last digit, turning 9s into 0s until a digit below 9 can be
    incremented, else prepend a 1.
Tricks: Stop at the first digit below 9; only when every digit was 9 does the array grow.
Edge cases:
  - All nines such as [9, 9, 9]
  - A single digit, 0 or 9
  - Carry that stops midway, such as [1, 9, 9]

Time O(n), space O(1).
"""

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        # Walk from the least significant digit. A digit below 9 absorbs the carry
        # and everything to its left stays as it is, so we can stop right there.
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0  # 9 + 1 = 10: write 0 and carry into the next digit
        # Every digit was a 9 and is now 0, so the number gains a leading 1.
        return [1] + digits
