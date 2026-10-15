"""Design Add and Search Words Data Structure (#211, medium)

Approach: Trie insert; search is a DFS that branches to every child on '.'.
Tricks: Only '.' branches; ordinary characters follow one edge.
Edge cases:
  - Pattern of only dots
  - Pattern longer than any stored word
  - Empty trie

Time O(L) add, O(26^L) worst-case search, space O(total chars).
"""

# Judge notes:
# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_1 = obj.search(word)


class WordDictionary:
    def __init__(self):
        # Trie as nested dicts: each key is a letter, "$" marks the end of a word.
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            # Walk down, creating missing nodes. Cost is O(len(word)).
            node = node.setdefault(ch, {})
        node["$"] = True  # a prefix alone is not a word; the marker says one ends here

    def search(self, word: str) -> bool:
        # dfs(node, i): can word[i:] be matched starting below this trie node?
        def dfs(node, i):
            # Consumed the whole word: it only counts if a word ends here.
            if i == len(word):
                return "$" in node
            ch = word[i]
            # Wildcard: try every child branch. Skip the "$" key, which is not a letter.
            # Worst case visits the whole trie, but plain letters follow a single path.
            if ch == ".":
                for key, child in node.items():
                    if key != "$" and dfs(child, i + 1):
                        return True
                return False
            # Ordinary letter: follow the one matching edge, or fail if absent.
            child = node.get(ch)
            return child is not None and dfs(child, i + 1)

        return dfs(self.root, 0)
