## The idea

A signal spreads along directed edges, taking each edge's weight in time. The time every node has heard it is the shortest-path distance from `k` to the farthest node. So this is single-source shortest paths with non-negative weights, which is Dijkstra's algorithm. The answer is the largest of the shortest distances, or `-1` if some node is never reached.

Summing weights or following the fewest edges does not work: a longer route in edges can be quicker in time.

## Set-up

- `graph` maps each node to a list of `(neighbour, weight)` pairs.
- `heap` holds `(distance, node)` candidates, smallest first. It starts as `[(0, k)]`.
- `dist` holds final distances. Invariant: once a node is in `dist`, its value is the true shortest distance, because weights are non-negative and we pop the smallest candidate first.

```text
times: 1->2 (1), 1->3 (5), 2->3 (1), 3->4 (1)      n = 4, k = 1

  1 --1--> 2
  1 --5--> 3
  2 --1--> 3
  3 --1--> 4

heap = [(0,1)]     dist = {}
```

## Step by step

Pop the smallest `(d, node)`. If `node` is already in `dist` it is a stale entry, skip it. Otherwise record `dist[node] = d` and push each unfinalised neighbour at `d + w`.

```text
pop (0,1)  dist={1:0}            push (1,2) (5,3)
           heap=[(1,2),(5,3)]

pop (1,2)  dist={1:0,2:1}        push (2,3)
           heap=[(2,3),(5,3)]

pop (2,3)  dist={1:0,2:1,3:2}    push (3,4)
           heap=[(3,4),(5,3)]

pop (3,4)  dist={1:0,2:1,3:2,4:3}
           heap=[(5,3)]

pop (5,3)  3 already in dist: stale, skip
           heap=[]
```

All 4 nodes are in `dist`, and `max(dist.values())` is `3`.

```text
shortest-path tree:   1 --1--> 2 --1--> 3 --1--> 4
distances:            0        1        2        3
```

Node 3 was first pushed at cost 5 by the direct edge, then at 2 via node 2. The cheaper entry popped first, and the 5 became stale.

## Why it works

The heap always yields the closest unfinished node. Any other route to it would have to pass through a node at least as far away, and with non-negative weights it can only get longer. So the first pop of a node is final, and skipping later pops is safe. Nodes never popped were never reachable, so `len(dist) == n` is exactly the "everyone got the signal" check.

## Where it goes wrong

- Not skipping stale entries wastes work and can overwrite a correct distance with a larger one if you assign without checking.
- Forgetting the count check: if `k` cannot reach node 4, `max(dist.values())` still returns a number. The `len(dist) == n` test turns that into `-1`.
- Returning the sum of distances instead of the maximum.

```text
times: 1->2 (1), 2->3 (2), n = 4, k = 1
dist = {1:0, 2:1, 3:3}   len 3 != 4  -> -1   (node 4 never heard it)
```

## Cost

Time O(E log V): each edge pushes at most once, and heap operations cost log. Space O(V + E): the graph plus the heap and `dist`.
