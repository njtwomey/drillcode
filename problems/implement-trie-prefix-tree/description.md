Implement a `Trie` class with these operations:

- `Trie()` creates an empty trie.
- `insert(word)` adds `word` to the trie. Returns nothing.
- `search(word)` returns `True` if exactly `word` was previously inserted, otherwise `False`. A string that is only a prefix of an inserted word does not count.
- `startsWith(prefix)` returns `True` if any previously inserted word begins with `prefix` (a whole word counts as its own prefix), otherwise `False`.

Constraints:
- `1 <= len(word), len(prefix) <= 2000`
- Strings contain only lowercase English letters.
- Up to `3 * 10^4` calls in total.
