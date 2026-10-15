"""Evaluate Division (#399, medium)

Approach: Build a weighted graph with edges a -> b of weight v and b -> a of 1/v, then
    BFS per query multiplying weights along the path.
Tricks: A variable absent from every equation gives -1.0 even for x / x, while a known x
    / x is 1.0; a weighted union-find also works.
Edge cases:
  - Unknown variable in a query
  - Query on two disconnected components
  - Same known variable on both sides

Time O(Q * (V + E)), space O(V + E).
"""

from collections import defaultdict, deque


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        # Each equation a / b = v gives two weighted edges: a -> b with weight v and
        # b -> a with weight 1 / v. A query x / y is the product of weights along any
        # path from x to y, since the chain of ratios telescopes.
        graph = defaultdict(dict)
        for (a, b), v in zip(equations, values):
            graph[a][b] = v
            graph[b][a] = 1 / v

        def solve(src: str, dst: str) -> float:
            # A variable that never appears in an equation has no known value, even
            # in x / x.
            if src not in graph or dst not in graph:
                return -1.0
            seen = {src}
            queue = deque([(src, 1.0)])
            while queue:
                curr, product = queue.popleft()
                if curr == dst:
                    return product
                for nxt, ratio in graph[curr].items():
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, product * ratio))
            return -1.0  # different components: the ratio is undetermined

        return [solve(a, b) for a, b in queries]
