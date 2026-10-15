Given a string `s`, return every way to split it into consecutive non-empty substrings such that each substring is a palindrome. The substrings in each partition, concatenated in order, must reproduce `s` exactly.

The partitions may be returned in any order, but the pieces within a partition must be in the order they appear in `s`.

Constraints:
- `1 <= len(s) <= 16`
- `s` contains only lowercase English letters
- The answer can be exponential in `len(s)`, so all partitions must be enumerated
