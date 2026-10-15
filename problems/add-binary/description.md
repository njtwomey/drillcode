Given two binary strings `a` and `b`, return their sum as a binary string. Each input is a non-empty string of `'0'` and `'1'` characters representing a non-negative integer, and the two may have different lengths.

The result has no leading zeros unless it is exactly `"0"`.

Constraints:
- `1 <= len(a), len(b) <= 10^4`
- Neither string has a leading zero, except the string `"0"` itself
- The values can be far larger than a 64-bit integer, so think about doing the addition digit by digit
