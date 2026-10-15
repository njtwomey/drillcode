"""Alien Dictionary (#269, hard)

Approach: Build an edge from the first differing character of each adjacent word pair;
    topological sort; a cycle means no valid order.
Tricks: Every letter that appears is a node, including those with no edges.
Edge cases:
  - A word followed by its own prefix ("abc", "ab") is invalid
  - Unconstrained letters may go in any order
  - Single word

Time O(C) total characters, space O(1) alphabet.
"""
from collections import deque


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # Graph: edge a -> b means "a comes before b". Every letter that appears is a
        # node, even if no rule mentions it, so it still appears in the output.
        edges = {c: set() for word in words for c in word}
        indegree = {c: 0 for c in edges}
        # Phase 1: only adjacent words give information. The FIRST differing letter is
        # the only one that tells us order; later letters say nothing.
        for first, second in zip(words, words[1:]):
            # "abc" before "ab" is impossible: a prefix must come first.
            if len(first) > len(second) and first.startswith(second):
                return ""
            for a, b in zip(first, second):
                if a != b:
                    # The set check stops duplicate edges inflating the indegree.
                    if b not in edges[a]:
                        edges[a].add(b)
                        indegree[b] += 1
                    break
        # Phase 2: Kahn's topological sort. Letters with indegree 0 have nothing that
        # must precede them, so they are safe to emit now.
        queue = deque(c for c in indegree if indegree[c] == 0)
        order = []
        while queue:
            c = queue.popleft()
            order.append(c)
            for nxt in edges[c]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        # If a cycle exists, its letters never reach indegree 0 and are never emitted,
        # so a short result means the rules contradict each other.
        return "".join(order) if len(order) == len(edges) else ""
