## The idea

Each equation `a / b = v` is a fact about how two variables relate. Chain facts together and you learn more: if `a / b = 2` and `b / c = 3`, then `a / c = 2 * 3 = 6`, because the `b` cancels. So a query `x / y` is answerable exactly when `x` and `y` are linked by a chain of equations, and the answer is the product of the ratios along the chain.

That is a graph problem. Variables are nodes, equations are weighted edges, and a query is a path search that multiplies weights as it goes.

## Set-up

- `graph[a][b]` is the ratio `a / b`. Each equation adds two edges: `a -> b` with weight `v`, and `b -> a` with weight `1 / v`, since flipping a fraction inverts it.
- `solve(src, dst)` answers one query with a breadth-first search.
- Inside it, `seen` stops us revisiting nodes, and `queue` holds `(node, product)` pairs, where `product` is the value of `src / node` so far. It starts at `1.0` because `src / src = 1`.

```text
equations: a/b = 2,  b/c = 3

   a ──2.0──▶ b ──3.0──▶ c
   a ◀─0.5─── b ◀─0.333─ c
```

## Step by step

Query `a / c`.

```text
start      queue = [(a, 1.0)]        seen = {a}

pop a      product 1.0
           neighbour b: new, push (b, 1.0 * 2.0 = 2.0)
           queue = [(b, 2.0)]        seen = {a, b}

pop b      product 2.0
           neighbour a: seen, skip
           neighbour c: new, push (c, 2.0 * 3.0 = 6.0)
           queue = [(c, 6.0)]        seen = {a, b, c}

pop c      c is the target: return 6.0
```

Two other queries on the same graph:

```text
a / a      a is in the graph, popped first, equals dst: 1.0
a / z      z is not in the graph at all:                -1.0
z / z      also -1.0: an unknown variable has no value, even over itself
```

If the graph had a separate component, say `x / y = 4`, then `a / x` would exhaust the queue without finding `x` and return `-1.0`.

## Why it works

Along any path, intermediate variables cancel, so the product of the edge weights equals `src / dst`. The equations are assumed consistent, so every path between the same two nodes gives the same product, and the first path BFS finds is as good as any. The reverse edge with weight `1 / v` is what lets us travel against the direction an equation was written.

## Where it goes wrong

Checking membership. The problem says an unknown variable answers `-1.0`, even for `x / x`. Without the `src not in graph` guard, the BFS would not run on a missing key and would either crash or return `1.0`.

Adding only one direction per equation means queries like `b / a` fail.

## Cost

Time O(Q * (V + E)): each query is a BFS over the graph. Building it is O(E). Space O(V + E) for the graph, plus O(V) per search.

## Other approaches

A weighted union-find answers each query in near constant time after the unions, at the cost of trickier code.
