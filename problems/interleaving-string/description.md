Given three strings `s1`, `s2` and `s3`, decide whether `s3` can be formed by interleaving `s1` and `s2`. An interleaving uses every character of both strings exactly once, merging them into one string while keeping the characters of each original string in their original relative order. Return `True` if possible, otherwise `False`. Either input may be empty.

Constraints:
- `0 <= len(s1), len(s2) <= 100`, `0 <= len(s3) <= 200`
- All strings consist of lowercase English letters
- Branching on every choice is exponential; O(m*n) time is the target
