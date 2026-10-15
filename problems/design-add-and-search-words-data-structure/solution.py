"""Design Add and Search Words Data Structure (#211, medium)

Approach: Trie insert; search is a DFS that branches to every child on '.'.
Tricks: Only '.' branches; ordinary characters follow one edge.
Edge cases:
  - Pattern of only dots
  - Pattern longer than any stored word
  - Empty trie

Time O(L) add, O(26^L) worst-case search, space O(total chars).
"""


class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                for key, child in node.items():
                    if key != "$" and dfs(child, i + 1):
                        return True
                return False
            child = node.get(ch)
            return child is not None and dfs(child, i + 1)

        return dfs(self.root, 0)
