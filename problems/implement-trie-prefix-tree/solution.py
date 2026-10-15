"""Nodes with a children dict and an end-of-word flag; all operations walk the prefix.

search and startsWith share the same walk, differing only in the final flag check.
Time O(L) per operation, space O(total chars).
"""


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
