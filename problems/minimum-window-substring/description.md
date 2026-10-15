Given strings `s` and `t`, return the shortest contiguous substring of `s` that contains every character of `t`, counting multiplicity (if `t` has two `"a"`, the window needs at least two). If no such substring exists, return `""`. The answer is guaranteed to be unique.

Constraints:
- `1 <= len(s), len(t) <= 10^5`
- Both strings contain upper- and lowercase English letters
- A solution better than O(`len(s)` * `len(t)`) is expected
