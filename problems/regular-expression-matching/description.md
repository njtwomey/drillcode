Given an input string `s` and a pattern `p`, decide whether the pattern matches the entire string (not just a part of it). The pattern supports two special characters: `.` matches any single character, and `*` matches zero or more copies of the character immediately before it. Return `True` on a full match, otherwise `False`.

Constraints:
- `1 <= len(s) <= 20` and `1 <= len(p) <= 20`
- `s` contains only lowercase letters
- `p` contains lowercase letters, `.` and `*`
- Every `*` follows a letter or `.`, so a `*` never starts the pattern or follows another `*`
