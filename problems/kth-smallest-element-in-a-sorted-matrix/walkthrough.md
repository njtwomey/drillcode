## The idea

Flattening and sorting the whole matrix works but ignores the structure. Every row is already sorted, so the smallest value you have not yet taken must be the first unused value of some row. You never have to look deeper than one candidate per row.

So keep one candidate per row in a min-heap. The top is the smallest value left. Take it, then replace it with the next value from the same row. After doing this `k - 1` times, the top of the heap is the `k`-th smallest. This is the same idea as merging `n` sorted lists, stopped early.

Columns are sorted too, so the `k`-th smallest cannot be below row `k` (there would already be `k` smaller values above it). Only the first `min(n, k)` rows are loaded.

## Set-up

- `n` is the side length.
- `heap` holds `(value, r, c)`: the value, and where it came from so we know what to push next. It starts with the first element of each of the first `min(n, k)` rows.
- Invariant: the heap holds exactly one unused value per row, the smallest unused one in that row.

Using the first test, `k = 8`:

```text
matrix            heap (smallest first)
 1   5   9        (1, r0, c0)
10  11  13        (10, r1, c0)
12  13  15        (12, r2, c0)
```

## Step by step

Pop `k - 1 = 7` times. After each pop, push the right neighbour if the row has one.

```text
pop 1   (r0,c0)  push 5      heap: 5   10  12
pop 5   (r0,c1)  push 9      heap: 9   10  12
pop 9   (r0,c2)  row ends    heap: 10  12
pop 10  (r1,c0)  push 11     heap: 11  12
pop 11  (r1,c1)  push 13     heap: 12  13
pop 12  (r2,c0)  push 13     heap: 13  13
pop 13  (r1,c2)  row ends    heap: 13
```

Seven values are gone: `1 5 9 10 11 12 13`. The top is `13`, the 8th smallest. Duplicate values are fine, because the heap compares the whole tuple and each copy is its own entry that gets counted once.

## Why it works

Before each pop, every unused value is either in the heap or behind a heap entry in its own row, and rows are sorted, so nothing behind an entry is smaller than it. That makes the heap top the global minimum of the unused values. Removing it `k - 1` times removes the `k - 1` smallest, leaving the `k`-th on top.

## Where it goes wrong

- Off-by-one on the pop count. This code pops `k - 1` times and then reads the top. Popping `k` times and also reading the top would return the (k+1)-th value.
- Forgetting the bounds check `c + 1 < n` would index past the row end.
- Treating equal values as one. In `[[1, 1], [1, 2]]` with `k = 3` the answer is `1`, because each `1` takes a place.

## Other approaches

Binary search on the value: pick a middle value, count how many entries are at most that value by walking the staircase from the bottom-left corner in O(n), and narrow the range. It costs O(n log range) and uses O(1) space, which wins when `k` is large.

## Cost

Time O(min(n, k) + k log min(n, k)): build the heap, then up to `k` pops and pushes on a heap of at most `min(n, k)` entries. Space O(min(n, k)) for the heap.
