## The idea

A square with sides parallel to the axes is fully decided by two opposite corners. If the query point is `(x, y)` and the corner diagonally across from it is `(px, py)`, the other two corners must be `(px, y)` and `(x, py)`. There is no freedom left.

So there is no need to search for triples of points. For each stored point, treat it as the diagonal corner, check that it makes a real square with the query, and look up the two forced corners. The brute force tries every triple of stored points, which is far too slow. This tries one point at a time and does two dictionary lookups.

Duplicates are allowed, and every copy counts as a different square. So we store counts, and the number of squares for one diagonal is the product of three counts.

## Set-up

- `self.points` is a `Counter` from `(x, y)` to how many times that point was added. It exists so that a lookup of a missing corner returns 0 instead of raising, and so that copies multiply.

`add` just bumps a count. All the work is in `count`.

```text
points after add (3,10), (11,2), (3,2):

  y
 10   (3,10):1
  .
  2   (3,2):1          (11,2):1
      x=3              x=11
```

## Step by step

Query `(11, 10)`. For every stored `(px, py)` we need `abs(px - x) == abs(py - y)` and `px != x`.

```text
 y
10   (3,10)                Q(11,10)

 2   (3,2)                  (11,2)
     x=3                    x=11

stored (3,10): dx = 8, dy = 0   unequal       skip
stored (11,2): dx = 0           px == x       skip
stored (3,2) : dx = 8, dy = 8   a square
    corner (px, y)  = (3,10)  count 1
    corner (x, py)  = (11,2)  count 1
    result += 1 * 1 * 1       result = 1
```

Now add `(11, 2)` a second time, so its count is 2, and ask again.

```text
stored (3,2): diag = 1, points[(3,10)] = 1, points[(11,2)] = 2
              result += 1 * 1 * 2     result = 2
```

Querying `(14, 8)` fails the equal-distance test for `(3,2)` (11 against 6), so the answer is 0.

## Why it works

For a fixed query, every square that uses it has exactly one corner diagonal to it. Looping over all stored points as that corner visits each possible square shape once. The other two corners are forced, so the number of ways to pick actual stored copies is `diag * points[(px, y)] * points[(x, py)]`. Summing over diagonals counts every square exactly once.

## Where it goes wrong

The `px == x` test matters. If the query itself is a stored point, its diagonal distance is `0 == 0`, which passes the equal-distance check but is a zero-area square.

```text
stored (5,5), query (5,5):  dx = 0, dy = 0   equal, but not a square
```

Also remember that `count` must not add the query point, and that a rectangle with unequal sides is rejected by the distance test.

## Cost

`add` is O(1). `count` loops over the `p` distinct stored points with O(1) lookups, so it is O(p). Space is O(p).
