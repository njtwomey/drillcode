"""Implement Trie (Prefix Tree) (#208, medium)

Approach: Node with a children map and an end-of-word flag; insert, search and
    startsWith walk the tree.
Tricks: search and startsWith share the same walk; only the final flag check differs.
Edge cases:
  - Prefix that is also a word
  - Word that is a prefix of a longer stored word

Time O(L) per operation, space O(total chars).
"""


class _TrieNode:
    def __init__(self):
        # One edge per next character; the path from the root spells the prefix.
        self.children = {}
        # Marks that a word ends here; needed to tell "app" from a mere prefix of "apple".
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

    # Shared by search and startsWith: follow prefix, return its end node or None.
    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        # Reaching the node is not enough; a word must actually end there.
        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        # Any existing path counts as a prefix, word or not.
        return self._walk(prefix) is not None
