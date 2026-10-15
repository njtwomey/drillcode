## The idea

Connecting all points at minimum total length is a minimum spanning tree on the complete graph where every pair has an edge with Manhattan distance as its weight. Prim's algorithm grows a tree from one point, and at each step attaches the outside point that is cheapest to link to the tree. Greedy works here because the cheapest edge crossing from the tree to the rest is always safe to take.

With n² edges, a heap offers no help. Instead keep one number per point and scan arrays.

## Set-up

- `cheapest[i]` is the lowest edge cost joining point `i` to the tree so far. It starts at infinity, with `cheapest[0] = 0` so point 0 is picked first.
- `visited[i]` marks points already in the tree.
- `total` is the cost accumulated.
- Each round: pick the unvisited `u` with the smallest `cheapest`, add it, then relax every unvisited `v` against `u`.

## Step by step

`points = [[0,0],[2,2],[3,10],[5,2],[7,0]]`, labelled 0 to 4.

```text
Round 1  cheapest = [0, inf, inf, inf, inf]
         pick u=0 (cost 0)            total 0
         relax: d(0,1)=4 d(0,2)=13 d(0,3)=7 d(0,4)=7
         cheapest = [0, 4, 13, 7, 7]

Round 2  pick u=1 (cost 4)            total 4
         relax: d(1,2)=9 < 13   d(1,3)=3 < 7   d(1,4)=7 not < 7
         cheapest = [0, 4, 9, 3, 7]

Round 3  pick u=3 (cost 3)            total 7
         relax: d(3,2)=10 not < 9   d(3,4)=4 < 7
         cheapest = [0, 4, 9, 3, 4]

Round 4  pick u=4 (cost 4)            total 11
         relax: d(4,2)=14 not < 9
         cheapest unchanged

Round 5  pick u=2 (cost 9)            total 20
```

The answer is 20, with tree edges 0-1 (4), 1-3 (3), 3-4 (4), 1-2 (9).

```text
  2 (3,10)
  │ 9
  1 (2,2) ── 3 (5,2) ── 4 (7,0)
  │ 4     3          4
  0 (0,0)
```

## Why it works

At any moment the tree is a connected piece, and the cheapest edge leaving it can always be part of some minimum spanning tree (the cut property). `cheapest[v]` stores exactly that cheapest edge for each outside point, and updating it whenever the tree grows keeps it correct.

## Where it goes wrong

- Forgetting to relax after adding `u` leaves stale `cheapest` values and a too-high total.
- The relaxation compares against the edge to `u` only, not the sum of the path from the start; this is not shortest paths, so never add `cheapest[u]` to the distance.
- One point: the loop runs once with cost 0, giving 0.

## Other approaches

`solution_kruskal.py` builds all n(n-1)/2 edges, sorts them, and uses union-find to take each edge that joins two separate components, stopping after n - 1 edges. It is easy to explain but costs O(n² log n) time and O(n²) space.

## Cost

Time O(n²): n rounds, each scanning n points twice. Space O(n) for the two arrays.
