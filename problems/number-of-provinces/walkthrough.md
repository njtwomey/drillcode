## The idea

Cities form a group (a province) if they are linked directly or through other cities. That is counting connected components, here given as an adjacency matrix. Start by saying every city is its own province. Each direct link between two cities in different provinces merges them and reduces the count by one. Union-find tracks which province each city is in.

Counting merges as they happen is simpler than counting roots at the end.

## Set-up

- `parent = list(range(n))`: every city is its own root.
- `find(x)` climbs to the root of `x`'s province and uses path halving (`parent[x] = parent[parent[x]]`) so the trees stay shallow without recursion.
- `count = n`. Invariant: it equals the number of distinct roots.
- The loops use `j in range(i + 1, n)` because the matrix is symmetric, so the upper triangle holds every link once.

```text
isConnected:      parent: [0, 1, 2]     count = 3
  1 1 0
  1 1 1
  0 1 1
```

## Step by step

For each pair `i < j` with a link, find both roots. If they differ, set `parent[root_i] = root_j` and decrement `count`.

```text
(0,1) linked  roots 0 and 1 differ
              parent[0] = 1      parent = [1, 1, 2]   count = 2

(0,2) is 0, no link, skipped (it is checked after (0,1) in row 0)

(1,2) linked  find(1)=1, find(2)=2 differ
              parent[1] = 2      parent = [1, 2, 2]   count = 1
```

```text
before        after (0,1)     after (1,2)

0  1  2        0 -> 1  2       0 -> 1 -> 2
```

One province remains, so the answer is `1`, even though cities 0 and 2 have no direct link. The chain through city 1 joined them.

## Why it works

Every link is examined once. Two linked cities end up with the same root: either they already had one, or the union gives them one. A merge only happens between different roots, so each merge takes two provinces to one. Cities not connected by any chain are never given the same root.

## Where it goes wrong

- Counting every `1` in the matrix. The diagonal is all ones and links appear twice, so the count would be wrong.
- Ignoring the root check. `(0,1)` linked twice through different paths must not decrement `count` twice.
- Merging `i` and `j` directly (`parent[i] = j`) instead of their roots. That can detach cities already in a province.

```text
0 and 1 already share root 1; 2 is alone. Link (0,2):
  wrong:  parent[0] = 2 (using i, not its root) would leave 1 behind:
          0 -> 2, while 1 is still its own root
  right:  parent[find(0)] = find(2), i.e. parent[1] = 2
```

## Cost

Time O(n^2 * alpha(n)): the matrix scan dominates, and each union-find step is nearly constant. Space O(n) for `parent`.
