Implement a class `WordDictionary` with these operations:

- `WordDictionary()` creates an empty dictionary.
- `addWord(word)` stores `word`; returns nothing. The same word may be added more than once.
- `search(word)` returns `True` if some previously added word matches `word`, otherwise `False`. A `.` in `word` matches any single letter; every other character must match exactly, and lengths must be equal.

Constraints:
- Words consist of lowercase English letters; queries may also contain `.`
- Word length at most 25
- Up to about 10^4 calls in total, with at most 2 dots per query
