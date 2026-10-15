Given two strings `word1` and `word2`, return the minimum number of single-character operations needed to turn `word1` into `word2`. The allowed operations are inserting a character, deleting a character, and replacing one character with another, each costing one. Either string may be empty.

Constraints:
- `0 <= len(word1), len(word2) <= 500`
- Both strings consist of lowercase English letters
- Exhaustive search over edit sequences is too slow; O(m*n) is the target
