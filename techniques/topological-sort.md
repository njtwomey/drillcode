---
title: Topological sort
area: Graphs
topics: [Graph]
problems:
  - course-schedule
  - course-schedule-ii
  - alien-dictionary
  - minimum-height-trees
related: [graph-building-and-dfs, bfs-shortest-paths, union-find]
---
## Reach for it when
- The statement has prerequisites or dependencies.
- It asks for an order in which every item comes after the items it depends on.
- It asks whether it is possible to finish, which means "is there a cycle".
- The order must be recovered from pairwise rules, such as sorted words in an unknown alphabet.

## Setup
- `graph` (or `edges`): an edge `a -> b` means a comes before b. For `[course, prereq]` the edge is `prereq -> course`.
- `indegree = [0] * n`, or a dict over every node: the number of unmet prerequisites of each node. Incremented once per edge.
- `queue = deque(i for i in range(n) if indegree[i] == 0)`: the nodes that can be taken now.
- A count or list of taken nodes (`done`, or `result` when the order itself is needed). It grows by one each time a node is popped.
- Invariant: a node enters the queue exactly when its `indegree` drops to 0. A node on a cycle never gets there.
- Result: a cycle exists if and only if fewer than `n` nodes were taken.

## Template
```python
from collections import deque


def topo_order(n, edges):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for a, b in edges:
        graph[a].append(b)
        indegree[b] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return result if len(result) == n else []
```

## What it removes
- It removes the cycle check as a separate pass. A short result is the check.
- It removes DFS with three states. Counting in-degrees finds the same cycles with a plain queue.
- It removes any sort. The order falls out of the queue.

## Pitfalls
- Leaving out isolated nodes. In alien dictionary every letter that appears is a node, built with `{c: set() for word in words for c in word}`. A letter with no rule is still part of the answer.
- Adding an edge for every differing character of two words. Only the first differing pair gives information; the solution `break`s after it.
- Treating a word followed by its own prefix (`"abc"` then `"ab"`) as valid. It is impossible, so return `""`.
- Duplicate edges inflating `indegree`. The alien dictionary solution checks `b not in edges[a]` before adding. Course schedule counts a duplicate prerequisite twice, which is also consistent because the decrement happens once per stored edge.
- A self-dependency `[a, a]` gives `a` an in-degree of 1 that nothing can reduce, so `a` is never taken and the answer is correctly false.
- Reading `len(result)` against the wrong total. In alien dictionary it is the number of distinct letters, `len(edges)`, not the number of words.

## Variants
- Feasibility only: `course-schedule` counts taken courses in `done` and returns `done == numCourses`. It names the arrays `graph` and `indegree` and the neighbour `nxt`.
- Order of courses: `course-schedule-ii` is the same loop with a `result` list in place of the `done` counter. It returns `result` if `len(result) == numCourses`, else `[]`.
- Recover the order: `alien-dictionary` builds the graph from adjacent word pairs, then fills `result`. It returns `""` when `len(result) != len(edges)` or when a prefix is out of order. Letters with no constraints come out in queue order, which is one valid answer.
- Leaf trimming on an undirected tree: `minimum-height-trees` is Kahn's idea with degree 1 in place of in-degree 0. `leaves` is the current layer, and `remaining` counts nodes left. Each pass removes the layer, pops the one neighbour of each leaf with `adj[leaf].pop()`, removes the leaf from that neighbour's set, and the neighbour joins `next_leaves` when its degree drops to 1. The loop stops when `remaining <= 2`, and the survivors are the centres. It handles `n <= 2` before building `adj`. There is no cycle check, since the input is a tree.
- The solutions use dicts and sets for the alien graph and lists for the course graph. The loop is the same.

## Worked example
Problem: `course-schedule`

The graph is built from the pairs, the zero in-degree courses are queued, and the loop counts how many are taken.

```python
class Solution:

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1
        queue = deque((i for i in range(numCourses) if indegree[i] == 0))
        done = 0
        while queue:
            node = queue.popleft()
            done += 1
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return done == numCourses
```

`graph` and `indegree` are the template's arrays. This solution keeps a count `done` instead of a `result` list because only feasibility is asked. The final comparison with `numCourses` is the "fewer than n taken means a cycle" test.
