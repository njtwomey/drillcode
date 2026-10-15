---
title: Trie patterns
area: Tries
topics: [Trie]
problems:
  - implement-trie-prefix-tree
  - design-add-and-search-words-data-structure
  - word-search-ii
  - maximum-xor-of-two-numbers-in-an-array
related: [backtracking-template, design-structures, grid-traversal, bit-tricks]
---
## Reach for it when

- The keys are integers and the question is about their bits, such as a maximum XOR.
- Many words are stored and queried by prefix.
- A search pattern has wildcards such as `.`.
- A grid must be searched for many words at once, where a separate search per word would repeat the same paths.
- Words share long prefixes and you want to pay for each shared prefix once.

## Setup

- `root`: an empty node. Invariant: the path of characters from the root to a node spells that node's prefix.
- A node is a mapping from character to child node, plus a marker that a word ends here. Two ways to hold it:
  - a class with `children = {}` and a flag such as `is_word`;
  - nested dicts, where a reserved key such as `"$"` marks the end. Storing the whole word under the marker means a search needs no reconstruction.
- For integers, the characters are bits `0` and `1`, read from the highest position down. Invariant: all numbers share the same depth, `max(nums).bit_length()`, so a path of that length is a whole number.
- `node = root` before every walk, then `node = node.get(ch)` for each character. Invariant: after processing `k` characters, `node` is the node for the first `k` characters, or `None` if there is none.
- For grid search, the DFS carries the current trie node as an argument. Invariant: the cell being visited holds a letter that is a child of that node.

## Template

```python
def trie_demo(words, word, prefix):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def walk(text):
        node = root
        for ch in text:
            node = node.get(ch)
            if node is None:
                return None
        return node

    found = walk(word)
    return found is not None and "$" in found, walk(prefix) is not None
```

`trie_demo(["apple"], "app", "app")` returns `(False, True)`: "app" is a prefix but not a stored word. Insert, search and prefix check all share one walk; only the last check differs.

## What it removes

- Scanning every stored word for each query. A lookup costs O(length of the query), independent of how many words are stored.
- Storing shared prefixes many times.
- In grid search, one DFS per word. One DFS over the trie follows all words together and abandons a path the moment no word has that prefix.

## Pitfalls

- Reporting a match after reaching a node without checking the end marker. Searching for `app` when only `apple` is stored wrongly returns true.
- Using `"$"` as a key and then iterating all children as if they were letters. In wildcard search the `"$"` key must be skipped on `.`.
- Not removing a found word in grid search. A word reachable by several paths is reported several times. Pop the marker when it is found.
- Walking the trie for letters that are not children. Check `board[nr][nc] in node` before recursing, or the DFS wanders through the board with no word to match.
- Forgetting to restore the board cell after the recursive call, so later start cells see `"#"`.
- Never pruning exhausted branches. Correct but slow on dense boards, since later searches walk dead subtrees.
- A binary trie that is shorter than the longest number or starts below its top bit. The top bits of the XOR are lost and the answer is too small.
- A pattern of only dots, or one longer than any stored word. The wildcard branch must return false when the word ends or children run out.

## Variants

- Plain trie, `implement-trie-prefix-tree`: a node class with `children` and `is_word`. A private `_walk(prefix)` returns the end node or `None`. `search` is `node is not None and node.is_word`, `startsWith` is `node is not None`.
- Wildcard search, `design-add-and-search-words-data-structure`: nodes are nested dicts. On a letter, follow the one edge. On `.`, try every child except the `"$"` marker and return true if any succeeds. `dfs(node, i)` asks whether `word[i:]` matches below `node`. Worst case is the whole trie, but plain letters follow one path.
- Grid search for many words, `word-search-ii`: build the trie with the word stored under `"$"`. The DFS marks the cell `"#"`, collects `node.pop("$", None)`, recurses into neighbours whose letter is a child, restores the cell, and deletes the child from its parent when the node is empty. See `backtracking-template` for the choose-recurse-undo shape.
- Binary trie, `maximum-xor-of-two-numbers-in-an-array`: nodes are dicts keyed by the bit, no end marker, because every path has the same length. Query each number by walking `1 - bit` when that key is in `node`, else `bit`, and build `current` with `current |= 1 << shift`. `best` is the largest `current`. See `bit-tricks`.

## Worked example

Problem: `implement-trie-prefix-tree`

A node class and a trie where `insert`, `search` and `startsWith` share one walk.

```python
class _TrieNode:

    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:

    def __init__(self):
        self.root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_word = True

    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

`root` is `self.root`, and `node` is the walking pointer set to it at the start of `insert` and `_walk`. `insert` creates missing children as it goes and sets `is_word` on the last node. `_walk` is the shared walk: it returns the node reached or `None`. `search` adds the end check on top of it and `startsWith` does not, which is the pitfall in the first bullet above.
