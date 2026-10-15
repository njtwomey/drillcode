Implement `myAtoi(s)`, which parses a leading integer from the string `s` the way C's `atoi` does. Skip leading space characters, accept one optional `+` or `-`, then read consecutive digits and stop at the first non-digit. Leading zeros are ignored. If no digits are read the result is `0`. Clamp the result to the signed 32-bit range `[-2^31, 2^31 - 1]` before returning it.

Constraints:
- `0 <= len(s) <= 200`
- `s` may contain letters, digits, spaces, `+`, `-` and `.`
