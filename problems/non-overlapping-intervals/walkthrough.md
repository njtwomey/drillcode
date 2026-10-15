## The idea

Removing the fewest intervals is the same as keeping the most intervals that do not overlap. That is the classic activity-selection problem. Trying every subset is exponential. Greedy works: always keep the interval that finishes earliest, because it leaves the most room for everything after it.

The answer is then the number of intervals we had to throw away.

## Set-up

- `intervals.sort(key=lambda i: i[1])` orders by end. This is what makes "finishes earliest" the next candidate every time.
- `last_end` is the end of the last interval we chose to keep. It starts as the end of the first sorted interval, which is always kept. Invariant: everything kept so far is mutually non-overlapping and ends at or before `last_end`.
- `removed` counts the discards.

```text
intervals: [1,2] [2,3] [1,3] [3,4]      (sorted by end)

time:   1    2    3    4
        [1───2]
             [2───3]
        [1─────────3]
                  [3───4]

last_end = 2, removed = 0
```

## Step by step

For each remaining `(start, end)`: if `start >= last_end` there is no overlap (touching is fine), so keep it and set `last_end = end`. Otherwise it overlaps the kept interval, which ends no later than this one, so drop it.

```text
[2,3]   2 >= 2 ?  yes -> keep      last_end = 3   removed = 0
[1,3]   1 >= 3 ?  no  -> drop                     removed = 1
[3,4]   3 >= 3 ?  yes -> keep      last_end = 4   removed = 1

kept:   [1,2] [2,3] [3,4]       dropped: [1,3]
```

The answer is `1`.

## Why it works

Among all intervals, the one with the smallest end can always be part of some best answer: swapping it in for whatever best-answer interval comes first cannot create a new overlap, since it ends no later. After keeping it, only intervals starting at or after its end remain usable, and the same argument applies again. When a candidate overlaps the kept one, it ends no earlier, so dropping it is never worse than dropping the kept one.

## Where it goes wrong

- Sorting by start. A long early interval then blocks many small ones. With `[1,100] [11,22] [1,11] [2,12]` the answer is 2 removals (keep `[1,11]` and `[11,22]`); sorting by start would keep the huge `[1,100]` first.
- Using `>` instead of `>=`. Intervals like `[1,2]` and `[2,3]` only touch, which is allowed, so they must both be kept.

```text
[1,2] [2,3]
  start 2 >= last_end 2   -> keep both, removed = 0
  with ">":  2 > 2 false  -> drops one, removed = 1 (wrong)
```

## Cost

Time O(n log n) for the sort; the scan is O(n). Space O(1) beyond the sort.
