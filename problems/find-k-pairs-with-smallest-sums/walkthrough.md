## The idea

There are `len(nums1) * len(nums2)` pairs, far too many to list and sort when we only want `k` of them. But both inputs are sorted, which gives a lot of structure.

Fix `i`. Then the sums `nums1[i] + nums2[j]` grow as `j` grows, so each `i` gives one sorted list. We want the `k` smallest values across all those lists, and a min-heap does exactly that: keep only the current front of each list, take the smallest, and replace it with the next item from the same list.

## Set-up

- `heap` holds tuples `(sum, i, j)`, the front of row `i`. It is seeded with `(nums1[i] + nums2[0], i, 0)` for the first `min(k, len(nums1))` values of `i`.
- `result` collects the answer pairs.

Why only `k` rows? Pair `(i, 0)` is beaten by `(0, 0)`, `(1, 0)`, up to `(i-1, 0)`. If `i >= k`, at least `k` pairs are already smaller, so row `i` can never reach the top `k`.

Invariant: the heap contains exactly one entry per row that still has pairs left, and it is that row's smallest unused pair.

```text
nums1 = [1, 7, 11]   nums2 = [2, 4, 6]   k = 4

heap = [(3, 0, 0), (9, 1, 0), (13, 2, 0)]
         1+2        7+2        11+2
```

## Step by step

```text
pop (3,0,0)   result [[1,2]]
              push (1+4, 0, 1) = (5,0,1)
              heap: (5,0,1) (9,1,0) (13,2,0)

pop (5,0,1)   result [[1,2],[1,4]]
              push (1+6, 0, 2) = (7,0,2)
              heap: (7,0,2) (9,1,0) (13,2,0)

pop (7,0,2)   result [[1,2],[1,4],[1,6]]
              j + 1 = 3 is past nums2: nothing to push
              heap: (9,1,0) (13,2,0)

pop (9,1,0)   result [[1,2],[1,4],[1,6],[7,2]]   len == k, stop
```

## Why it works

The smallest unused pair overall is always the front of some row, because each row is sorted. The heap holds every row's front, so its minimum is the global minimum of unused pairs. Popping it and exposing that row's next element keeps the invariant. After `k` pops we have taken the `k` smallest in order.

## Where it goes wrong

Forgetting the bound `j + 1 < len(nums2)` before pushing, which gives an index error on the last column.

Seeding the heap with all of `nums1` works but wastes time and memory when `nums1` is huge. And if `k` exceeds the number of pairs, the heap runs dry first, so the loop checks `heap` as well as `len(result) < k`.

Ties in the sum are fine: the tuple falls back to comparing `i` and `j`, which are integers.

## Cost

Time O(k log k): the heap never holds more than `min(k, len(nums1))` entries, and we do up to `k` pops and pushes. Space O(k) for the heap and the result.
