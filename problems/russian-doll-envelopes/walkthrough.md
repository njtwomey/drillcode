## The idea

An envelope fits in another only when both its width and height are strictly smaller. That is a two-dimensional condition. Sort by width, and the width part is mostly handled: you just need a chain of strictly increasing heights in the sorted order. That is the longest increasing subsequence (LIS) problem, which has an O(n log n) solution.

One catch: envelopes with the same width cannot nest, yet a plain sort could put them in increasing height order, and the LIS would chain them. Sorting equal widths by height descending prevents that, because within a group of equal widths heights fall, so no two of them can both join a strictly increasing chain.

## Set-up

- `envelopes.sort(key=lambda e: (e[0], -e[1]))` sorts by width ascending and height descending.
- `tails` is the LIS state. `tails[k]` is the smallest possible last height of a strictly increasing chain of length `k + 1`. It is always sorted.
- For each height, `bisect_left(tails, height)` finds its slot `i`.

```text
envelopes: [5,4] [6,4] [6,7] [2,3]
sorted:    [2,3] [5,4] [6,7] [6,4]
heights:     3     4     7     4
tails = []
```

## Step by step

```text
height 3   i=0, equals len(tails): append   tails = [3]
height 4   i=1, append                       tails = [3, 4]
height 7   i=2, append                       tails = [3, 4, 7]
height 4   i=1, tails[1] is already 4:       tails = [3, 4, 7]
           replace with itself, no growth
```

`len(tails)` is 3, the chain `[2,3] → [5,4] → [6,7]`. The last envelope `[6,4]` would have been a candidate to follow `[5,4]`, but widths 5 < 6 and heights 4 and 4 are equal, so it cannot nest. The strict `bisect_left` stops it.

## Why it works

If `i` equals `len(tails)`, the height beats every chain end and the longest chain grows by one. Otherwise it replaces `tails[i]`, a larger or equal end for chains of that length. A smaller end is never worse, because it can be extended by more future heights. The length of `tails` is the longest chain.

## Where it goes wrong

Sorting heights ascending on ties gives wrong answers. Take `[4,5] [4,6] [6,7] [2,3] [1,1]`:

```text
ascending ties:   (1,1)(2,3)(4,5)(4,6)(6,7)  heights 1 3 5 6 7 -> 5  wrong
                  (4,5) and (4,6) share a width, so they cannot nest
descending ties:  (1,1)(2,3)(4,6)(4,5)(6,7)  heights 1 3 6 5 7
                  tails: [1] [1,3] [1,3,6] [1,3,5] [1,3,5,7] -> 4  right
```

Using `bisect_right` instead of `bisect_left` would let equal heights extend a chain.

## Cost

Time O(n log n): the sort plus one binary search per envelope. Space O(n) for `tails` in the worst case.
