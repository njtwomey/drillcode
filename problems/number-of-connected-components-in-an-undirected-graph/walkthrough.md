## The idea

Counting components by walking the graph (DFS or BFS) works, but there is a neater way: start by pretending every node is its own component, then let each edge merge two components into one. Each real merge lowers the count by one. Edges that join nodes already in the same component (duplicates, self-loops, cycles) change nothing.

Union-find is the structure that answers "are these two already together?" in near constant time.

## Set-up

- `parent = list(range(n))`: every node is its own root. Following `parent` from any node leads to its component's root.
- `size = [1] * n`: component sizes, only meaningful at roots. Used to hang the smaller tree under the larger one, which keeps trees shallow.
- `find(x)` walks up to the root and does path halving on the way (`parent[x] = parent[parent[x]]`) so later walks are shorter.
- `components = n`: the running count. Invariant: it equals the number of distinct roots.

```text
n = 6   edges: (0,1) (2,3) (1,2) (4,5)

node:    0  1  2  3  4  5
parent:  0  1  2  3  4  5
size:    1  1  1  1  1  1
components = 6
```

## Step by step

For each edge find both roots. If they match, skip. Otherwise attach the smaller root under the larger (`parent[rb] = ra`), add the sizes and decrement `components`.

```text
(0,1)  roots 0,1 differ  parent[1]=0  size[0]=2  components=5
(2,3)  roots 2,3 differ  parent[3]=2  size[2]=2  components=4
(1,2)  find(1)=0, find(2)=2 differ
       sizes equal       parent[2]=0  size[0]=4  components=3
(4,5)  roots 4,5 differ  parent[5]=4  size[4]=2  components=2

final parent: [0, 0, 0, 2, 4, 4]

   0        4
  / \       |
 1   2      5
     |
     3
```

Two roots remain (0 and 4), so the answer is `2`.

## Why it works

Each node's root labels its component. Merging two different roots joins exactly two components, so the count drops by exactly one. If the roots are equal, the nodes are already connected and the edge adds nothing. After all edges, `components` is `n` minus the number of successful merges, which is the number of components.

## Where it goes wrong

- Comparing `parent[a]` with `parent[b]` instead of the roots. Only `find` gives the root.
- Decrementing the count on every edge. A duplicate edge `(0,1)` after `(0,1)` finds equal roots and must not count.
- Forgetting the `continue` for equal roots would let a cycle edge corrupt `size`.

```text
n = 3, edges (0,1) (1,2) (2,0)
  third edge: find(2) == find(0) -> skip, components stays 1
  counting every edge: 3 - 3 = 0   (wrong)
```

## Cost

Time O(n + E * alpha(n)), where alpha is the inverse Ackermann function, effectively constant. Space O(n) for `parent` and `size`.
