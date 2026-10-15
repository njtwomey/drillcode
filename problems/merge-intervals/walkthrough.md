## The idea

If intervals are sorted by start, any overlap must be with the interval just before. Anything earlier ended at or before that one begins, or was already merged into it. So we only ever compare each interval to the last merged one.

## Set-up

- `sorted(intervals)` orders by start (ties by end).
- `merged` is the result list, built up as we go. Its last entry is the only one that can still grow.
- Invariant: the entries of `merged` are disjoint and sorted, and cover everything seen so far.

## Step by step

`intervals = [[8,10],[1,3],[2,6],[15,18],[6,7]]`. Sorted: `[1,3], [2,6], [6,7], [8,10], [15,18]`.

```text
[1,3]    merged empty                    append
         merged = [[1,3]]

[2,6]    2 <= 3, overlap                 last end = max(3, 6) = 6
         merged = [[1,6]]

[6,7]    6 <= 6, touching counts         last end = max(6, 7) = 7
         merged = [[1,7]]

[8,10]   8 <= 7 ? no                     append
         merged = [[1,7], [8,10]]

[15,18]  15 <= 10 ? no                   append
         merged = [[1,7], [8,10], [15,18]]
```

On a number line (one column per unit, 1 to 18):

```text
          1         10
 1234567890123456789  (digits wrap at 10)
 [1,3]     ###
 [2,6]      #####
 [6,7]           ##
 [8,10]            ###
 [15,18]                 ####
 result    #######  ###     ####
```

## Why it works

After sorting, when we reach an interval its start is at least every earlier start. If it begins no later than the last merged end, it touches the last merged block and extends it. If it begins after, no later interval can reach back to the gap either, because later starts are even larger, so the last block is finished.

## Where it goes wrong

- Taking `merged[-1][1] = end` instead of `max(...)` breaks the nested case: `[1,10]` then `[2,3]` would shrink the block to `[1,3]`.
- Using `<` instead of `<=` leaves `[1,4]` and `[4,5]` unmerged, though they touch.
- Forgetting to sort first makes the "only compare with the last" shortcut wrong.

## Cost

Time O(n log n), dominated by the sort; the merge pass is O(n). Space O(n) for the output (plus the sorted copy).
