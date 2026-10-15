"""Word Search II (#212, hard)

Approach: Build a trie from the words; DFS the grid following trie edges, collecting
    words at end markers.
Tricks: Clear a word's end flag once found to avoid duplicates and prune later searches.
Edge cases:
  - Words sharing prefixes
  - a word that is a prefix of another
  - Words longer than the grid

Time O(m·n·3^L), space O(total chars).
"""


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Build a trie so one grid DFS searches for all words at once, and a path that
        # matches no word's prefix is abandoned immediately. Nodes are dicts; the "$"
        # key marks the end of a word and stores the word itself.
        root = {}
        for word in words:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = word

        rows, cols = len(board), len(board[0])
        found = []

        # dfs(r, c, parent): board[r][c] is already known to be a child of `parent`.
        def dfs(r, c, parent):
            ch = board[r][c]
            node = parent[ch]
            # pop (not get) so each word is reported once, even if reachable via
            # several paths.
            word = node.pop("$", None)
            if word is not None:
                found.append(word)
            board[r][c] = "#"  # mark as used on this path; "#" is never in the trie
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                # Checking the trie before recursing prunes dead-end prefixes.
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                    dfs(nr, nc, node)
            board[r][c] = ch  # backtrack
            # Prune exhausted trie branches (all words below found) so later searches
            # don't walk them again; this is a big speedup on dense boards.
            if not node:
                del parent[ch]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root:
                    dfs(r, c, root)
        return found
