Given strings `s` and `t`, return the number of distinct subsequences of `s` that equal `t`. Two subsequences are different if they use different sets of positions in `s`, even when the characters read the same. The answer is guaranteed to fit in a signed 32-bit integer.

Constraints:
- `1 <= len(s), len(t) <= 1000`
- Both strings consist of English letters
- Enumerating subsequences is exponential; O(m*n) time is the target
