Decode an encoded string `s`. The encoding rule is `k[text]`, meaning `text` is repeated exactly `k` times, where `k` is a positive integer that may have several digits. Groups may be nested and may sit next to plain letters or other groups. Return the fully expanded string.

The input is always well formed: brackets match, there are no stray digits, and a digit sequence appears only as a repeat count directly before `[`.

Constraints:
- `1 <= len(s) <= 30`
- `s` contains lowercase and uppercase letters, digits, and `[` `]`
- Repeat counts are in `[1, 300]`
- The decoded length stays below `10^5`
