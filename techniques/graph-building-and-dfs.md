---
title: Graph building and copying
area: Graphs
topics: [Graph, Hash, Linked list]
problems:
  - clone-graph
  - copy-list-with-random-pointer
  - course-schedule
  - is-graph-bipartite
  - evaluate-division
related: [topological-sort, union-find, grid-traversal, bfs-shortest-paths]
---
## Reach for it when
- Nodes and edges are given explicitly, as an edge list or as node objects with neighbours.
- The structure must be cloned, and its pointers may form cycles or point forward.
- You need to count components or detect a cycle.
- The edges come as pairs such as `[course, prerequisite]` and you need adjacency to walk them.

## Setup
- `adj`, the adjacency list. Use `graph = [[] for _ in range(n)]` for nodes numbered `0..n-1`, or `defaultdict(list)` for arbitrary labels. For an undirected edge, add both directions. For a directed edge, add one, from the node that must come first.
- `visited = set()` for a walk: a node is added when first reached, so it is expanded once. A walk can use recursive `dfs(u)` or an explicit `stack`.
- `copies = {}` for cloning: it maps each original node to its copy. It also serves as the visited set.
- Invariant for cloning: a node's copy is stored in `copies` before its neighbours are processed, so a cycle finds the copy instead of looping.
- An optional `None` entry: `copies = {None: None}` removes the special case for a null pointer.

## Template
```python
from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


def clone(start):
    if start is None:
        return None
    copies = {start: Node(start.val)}
    queue = deque([start])
    while queue:
        curr = queue.popleft()
        for neighbour in curr.neighbors:
            if neighbour not in copies:
                copies[neighbour] = Node(neighbour.val)
                queue.append(neighbour)
            copies[curr].neighbors.append(copies[neighbour])
    return copies[start]
```

## What it removes
- The map from original to copy removes any need to search for "the copy of this node". Every edge is wired by one lookup.
- Storing the copy first removes the infinite recursion on cycles.
- Two passes over a list with random pointers (create all copies, then wire) remove the problem of a pointer to a node that has not been copied yet.
- `{None: None}` removes the null check on `next` and `random`.

## Pitfalls
- Storing the copy after recursing into the neighbours. A cycle creates a second copy of the same node, or recurses forever.
- Forgetting the second direction of an undirected edge. Half the nodes look unreachable.
- Searching from one node only. A disconnected graph needs a start from every unvisited node (`is-graph-bipartite` loops over all `start` values; an odd cycle in a later component is missed otherwise).
- Self-loops and duplicate edges in the input. A self-loop is a cycle of length one; duplicates inflate an in-degree count unless guarded.
- Cloning only the node and not its neighbour list. The copy then still points at original nodes.
- Cycle detection on a directed graph with a single visited set. Reaching a finished node is fine; only reaching a node still in progress is a cycle. Use three states, or count in-degrees as `course-schedule` does.
- An empty input. `clone-graph` returns `None` for a null node.

## Variants
- Clone by BFS: `clone-graph` keeps `copies` and a queue. Its version is iterative, so there is no recursion to overflow. The mark on first sighting is the `copies` entry.
- Clone by two passes: `copy-list-with-random-pointer` is a graph with two edges per node. Pass 1 creates a copy per node, pass 2 wires `next` and `random` through the map.
- Build then process: `course-schedule` builds `graph` and `indegree` from the pairs, then runs Kahn's algorithm. See `topological-sort`.
- Two-colouring: `is-graph-bipartite` keeps `colour`, a dict from node to 0 or 1, which is also the visited set. It starts a BFS from every node not yet coloured, because the graph may be disconnected, gives each new neighbour `1 - colour[curr]`, and returns `False` when an already-coloured neighbour has the same colour as `curr`. An odd cycle is the only way this happens.
- Weighted edges: `evaluate-division` stores `graph[a][b] = v` and `graph[b][a] = 1 / v`, then runs a BFS per query carrying `product`. A variable missing from `graph` gives `-1.0` even for `x / x`; different components also give `-1.0`.
- Components and cycles in an undirected graph: `union-find` does it without a walk.
- The O(1) space version of the list copy interleaves copies after the originals. The catalogue solution uses the map.

## Worked example
Problem: `clone-graph`

The `copies` dict is the visited set and the original-to-copy map at once. A neighbour seen for the first time gets its copy immediately and is queued.

```python
class Solution:

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        copies = {node: Node(node.val)}
        queue = deque([node])
        while queue:
            curr = queue.popleft()
            for neighbour in curr.neighbors:
                if neighbour not in copies:
                    copies[neighbour] = Node(neighbour.val)
                    queue.append(neighbour)
                copies[curr].neighbors.append(copies[neighbour])
        return copies[node]
```

`copies` is the template's map. The copy is stored before the neighbour is queued, so the neighbour's own neighbours can point back at it. The line `copies[curr].neighbors.append(...)` runs once per edge, from its source side, so each edge is copied once.
