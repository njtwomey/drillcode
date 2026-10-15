"""Multiply Strings (#43, medium)

Approach: Schoolbook multiplication into a result array of length m + n, adding each
    digit product at position i + j + 1 and carrying to i + j.
Tricks: Add into the existing column value before splitting into digit and carry, then
    strip at most one leading zero; return "0" up front if either input is zero.
Edge cases:
  - Either operand is "0"
  - Long operands with long carry chains
  - Product with a trailing run of zeros
  - Product has m + n - 1 digits

Time O(m * n), space O(m + n).
"""

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        # Schoolbook multiplication. An m-digit by n-digit product has at most m + n
        # digits, and digit i of num1 times digit j of num2 lands in column i + j + 1
        # (carry into i + j); columns are indexed from the left, like the strings.
        result = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # Add into the column's existing value so earlier partial products and
                # carries are folded in right away; the sum stays below 100.
                total = (ord(num1[i]) - 48) * (ord(num2[j]) - 48) + result[i + j + 1]
                result[i + j + 1] = total % 10
                result[i + j] += total // 10
        # Neither input is zero here, so the product has m + n or m + n - 1 digits;
        # drop at most one leading zero.
        start = 1 if result[0] == 0 else 0
        return "".join(str(d) for d in result[start:])
