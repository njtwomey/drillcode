## The idea

Picking index `i` with probability `w[i] / total` is the same as throwing a dart at a line of length `total`, where index `i` owns a segment of length `w[i]`. A uniform dart lands in a segment with probability proportional to its length.

So build the segments, pick a uniform integer target, and find which segment it fell into. The segments are consecutive, so their right edges are the running totals of the weights. That is a sorted list, and finding the segment is a binary search.

The naive way is to expand each index `w[i]` times into a big list and pick from it. With weights up to 100000 that list is huge. Prefix sums keep the same idea in O(n) memory.

## Set-up

- `self.prefix` is the running sum: `prefix[i]` is the total weight of indices `0..i`. It is the right edge of index `i`'s block, and it is sorted because weights are positive.
- `self.total` is `prefix[-1]`, the number of targets there are.

Index `i` owns the integer targets in `(prefix[i-1], prefix[i]]`, which is exactly `w[i]` of them.

```text
w      = [3, 1, 2]
prefix = [3, 4, 6]        total = 6

target:   1  2  3 | 4 | 5  6
index :   0  0  0 | 1 | 2  2
          block 0   blk1  block 2
```

## Step by step

`pickIndex` draws `target = random.randint(1, total)`, which includes both ends, then returns `bisect_left(prefix, target)`. That is the first position whose prefix is at least the target.

```text
target 1 -> first prefix >= 1 is 3 (pos 0)   index 0
target 3 -> first prefix >= 3 is 3 (pos 0)   index 0
target 4 -> first prefix >= 4 is 4 (pos 1)   index 1
target 5 -> first prefix >= 5 is 6 (pos 2)   index 2
target 6 -> first prefix >= 6 is 6 (pos 2)   index 2
```

Index 0 got 3 of 6 targets, index 1 got 1, and index 2 got 2, matching the weights.

## Why it works

Each target from 1 to `total` maps to exactly one index, and index `i` receives exactly `w[i]` targets. With a uniform target, the chance of `i` is `w[i] / total`. `bisect_left` returns the first prefix that is not below the target, which is the block whose right edge covers it.

## Where it goes wrong

The range of the target and the choice of `bisect_left` have to agree. If you draw from `0..total-1` but still use `bisect_left`, targets 0, 1, 2 and 3 all land on index 0, because `prefix[0] == 3` already satisfies 3.

```text
w = [3, 1, 2], target in 0..5, bisect_left:
 target: 0 1 2 3 | 4 | 5
 index : 0 0 0 0 | 1 | 2     index 0 gets 4 of 6, should be 3
```

Use `1..total` with `bisect_left`, or `0..total-1` with `bisect_right`.

## Cost

The constructor is O(n) for the prefix sums. `pickIndex` is O(log n) for the binary search. Space is O(n).
