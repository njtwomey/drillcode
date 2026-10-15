## The idea

A graph is bipartite if its nodes can be split into two teams so that every edge joins different teams. Equivalently: colour the nodes with two colours so no edge has both ends the same colour. Once you colour one node, all its neighbours are forced to the opposite colour, their neighbours forced back, and so on. A contradiction means the graph has an odd cycle and cannot be split.

So the algorithm is just: colour greedily by following edges, and report failure if an edge ever joins two equal colours.

## Set-up

- `colour` is a dict from node to 0 or 1. A node missing from it has not been reached.
- The outer loop `for start in range(len(graph))` begins a new search at any node that is still uncoloured. The graph may be disconnected, and each component needs its own start.
- `queue` is a BFS queue holding nodes whose neighbours still have to be examined.

Invariant: every coloured node's colour is consistent with every edge already checked.

## Step by step

Graph: `0:[1,2,3]  1:[0,2]  2:[0,1,3]  3:[0,2]`, a triangle 0-1-2 plus extra node 3.

```text
start = 0:   colour = {0: 0},  queue = [0]

pop 0 (colour 0). Neighbours 1, 2, 3 are uncoloured -> colour 1.
             colour = {0:0, 1:1, 2:1, 3:1}
             queue  = [1, 2, 3]

pop 1 (colour 1).
   neighbour 0: colour 0, differs from 1, fine.
   neighbour 2: colour 1, SAME as curr's colour 1  -> return False

    0 (0)
   /|\
  1 2 3      1, 2 and 3 are all coloured 1, but 1 and 2 are joined
 (1)(1)(1)   by an edge: the triangle 0-1-2 is an odd cycle.
```

Now a graph that works, the four-cycle `0:[1,3] 1:[0,2] 2:[1,3] 3:[0,2]`:

```text
colour 0 -> 0.  Neighbours 1, 3 get 1.
pop 1: neighbour 0 is 0 (ok), neighbour 2 uncoloured -> 0.
pop 3: neighbours 0 (0) and 2 (0) both differ from 1, fine.
pop 2: neighbours 1 and 3 are 1, differ from 0, fine.   -> True

  0(0) ─ 1(1)
   │      │
  3(1) ─ 2(0)
```

## Why it works

If a valid 2-colouring exists, a node's colour fixes its neighbours' colours, so the colouring of each connected component is forced once you pick the start colour. BFS therefore finds the only possible colouring, and the conflict check proves that none exists when it fails. A conflict across a BFS edge means two same-coloured nodes are joined, and both reach the start by paths whose lengths have equal parity, which closes an odd cycle.

## Where it goes wrong

- Starting BFS only from node 0. A later component may hold the odd cycle, as in `[[1],[0],[3,4],[2,4],[2,3]]`, where nodes 2, 3 and 4 form a triangle.
- Skipping the `elif` check. Colouring new nodes without testing already-coloured neighbours misses the conflicts entirely.
- Isolated nodes have empty neighbour lists and are fine; they simply get colour 0.

## Cost

Time O(V + E): every node is queued once and every edge is examined from both ends. Space O(V) for `colour` and the queue.
