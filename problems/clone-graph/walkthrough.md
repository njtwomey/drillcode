## The idea

Copying a tree is easy because there is only one way to reach each node. A graph can have cycles and several routes to the same node, so a plain copy would either loop forever or clone a node twice and end up with a graph whose edges lead to different copies of the same node.

The fix is a dictionary from original node to its clone. It does two jobs. It tells you whether a node has already been cloned (so each is cloned once and cycles stop), and it lets you look up the clone to wire an edge to.

## Set-up

- `copies` maps original to clone. It starts with `{node: Node(node.val)}`.
- `queue` holds originals whose clones exist but whose neighbour lists are not yet filled in. It starts with `node`. (A `None` input returns `None` first.)
- The invariant: a node is in `copies` from the moment it is first seen, and in `queue` once, so each is processed once.

The graph, with node numbers as values:

```text
1 ─── 2
│     │
4 ─── 3

neighbours:  1:[2,4]  2:[1,3]  3:[2,4]  4:[1,3]
```

## Step by step

Primes mark clones. Each processed node fills in its clone's neighbour list.

```text
Start     copies {1:1'}           queue [1]

pop 1     neighbour 2: new, make 2', queue it.   1'.neighbors [2']
          neighbour 4: new, make 4', queue it.   1'.neighbors [2', 4']
          copies {1,2,4}          queue [2, 4]

pop 2     neighbour 1: known.                    2'.neighbors [1']
          neighbour 3: new, make 3', queue it.   2'.neighbors [1', 3']
          copies {1,2,3,4}        queue [4, 3]

pop 4     neighbour 1: known.                    4'.neighbors [1']
          neighbour 3: known.                    4'.neighbors [1', 3']
          queue [3]

pop 3     neighbour 2: known.                    3'.neighbors [2']
          neighbour 4: known.                    3'.neighbors [2', 4']
          queue []
```

Return `copies[node]`, the clone of node 1. Its neighbour lists match the original's, but every node is a new object.

## Why it works

Each original node is cloned exactly once, at first sight, so every edge in the copy points to the one clone of its target. Each edge is added from its source's side when the source is popped, so each directed edge is copied exactly once (and an undirected edge appears once in each endpoint's list, just like the original).

## Where it goes wrong

Creating the clone only when a node is popped, instead of when it is first seen. Then a node can be queued by several neighbours before anyone processes it:

```text
pop 2 queues 3, pop 4 also queues 3, because 3 is not cloned yet
3 gets cloned twice and the edges point at different copies
```

Creating the clone at the moment of discovery, as the code does, closes that gap. A single node with no neighbours works as is: one clone, empty list.

## Other approaches

DFS with recursion and the same dictionary works too. The rule is identical: put the clone in the dictionary before recursing into neighbours, or a cycle recurses forever. BFS avoids deep recursion on long chains.

## Cost

Time O(V + E): every node is cloned once and every edge copied once. Space O(V) for `copies` and the queue.
