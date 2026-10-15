"""Build a trie from the words, then DFS from every cell following trie edges,
collecting a word when its end marker is reached. The marker is cleared once
found (no duplicates) and exhausted trie branches are pruned.

Time O(m*n*3^L), space O(total chars).
"""


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = {}
        for word in words:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = word

        rows, cols = len(board), len(board[0])
        found = []

        def dfs(r, c, parent):
            ch = board[r][c]
            node = parent[ch]
            word = node.pop("$", None)
            if word is not None:
                found.append(word)
            board[r][c] = "#"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                    dfs(nr, nc, node)
            board[r][c] = ch
            if not node:
                del parent[ch]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root:
                    dfs(r, c, root)
        return found
