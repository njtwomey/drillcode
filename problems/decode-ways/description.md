A message of digits is encoded from letters using `A -> 1`, `B -> 2`, ..., `Z -> 26`. Given the digit string `s`, return the number of ways to split it into groups that each map to a letter. Groups with leading zeros (such as `06`) are invalid, and `0` alone is invalid. Return `0` if no valid decoding exists.

Constraints:
- `1 <= len(s) <= 100`
- `s` contains only digits and may start with `0`.
- The answer fits in a 32-bit integer.
