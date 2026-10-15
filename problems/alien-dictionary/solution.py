"""Compare adjacent words; the first differing letters give an edge a -> b.
Every letter seen is a node. Kahn's topological sort; a cycle or a word followed
by its own proper prefix means no valid order, so return "".

Time O(C) over total characters, space O(1) (alphabet-bounded graph).
"""
from collections import deque


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        edges = {c: set() for word in words for c in word}
        indegree = {c: 0 for c in edges}
        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""
            for a, b in zip(first, second):
                if a != b:
                    if b not in edges[a]:
                        edges[a].add(b)
                        indegree[b] += 1
                    break
        queue = deque(c for c in indegree if indegree[c] == 0)
        order = []
        while queue:
            c = queue.popleft()
            order.append(c)
            for nxt in edges[c]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return "".join(order) if len(order) == len(edges) else ""
