## The idea

The list is already sorted and has no overlaps, so the new interval can only interact with a contiguous run of existing ones. Everything before that run ends too early to matter, everything after it starts too late. So walk once, left to right, in three phases: copy the early ones, absorb the overlapping ones into the new interval, copy the rest.

Sorting everything again and merging would cost O(n log n) and does extra work; the structure of the input makes one pass enough.

## Set-up

- `start, end` is the new interval, which will grow as we absorb neighbours.
- `i` is the single index that advances through `intervals` across all three phases.
- `result` collects the output in order.

Invariant: everything already in `result` is final and lies strictly left of `[start, end]`.

```text
intervals = [1,2] [3,5] [6,7] [8,10] [12,16]     new = [4,8]
             ^ i
```

## Step by step

Phase 1 copies while `intervals[i][1] < start`, i.e. the interval ends before the new one begins.

```text
[1,2]: 2 < 4  -> copy.           result = [[1,2]]
[3,5]: 5 < 4? no -> phase 1 ends, i points here.
```

Phase 2 absorbs while `intervals[i][0] <= end`, i.e. the interval starts no later than the new one ends. It widens `start` and `end`.

```text
 start,end = 4,8
 [3,5]:  3 <= 8 -> start = min(4,3) = 3, end = max(8,5) = 8
 [6,7]:  6 <= 8 -> start = 3,           end = max(8,7) = 8
 [8,10]: 8 <= 8 -> start = 3,           end = max(8,10) = 10
 [12,16]: 12 <= 10? no -> phase 2 ends.
```

Phase 3 appends `[3, 10]`, then the untouched tail.

```text
number line:
   1 2 3 4 5 6 7 8 9 10 11 12 ... 16
   ├─┤                                 copied
     ├───┤                             [3,5] absorbed
          ├─┤                          [6,7] absorbed
               ├──┤                    [8,10] absorbed
        ├────────┤                     new [4,8]  ->  merged [3,10]
                          ├────────┤   [12,16] copied

result = [[1,2], [3,10], [12,16]]
```

## Why it works

An interval entirely before the new one satisfies `end_i < start`; because the list is sorted, once one fails that test all later ones also start at or after `start`. Likewise, once an interval starts after `end`, all later ones do too. The run in between is exactly the set that overlaps, and merging them is just taking the minimum start and maximum end.

## Where it goes wrong

- Using `<=` in phase 1 would treat an interval ending exactly at `start` as non-overlapping, but touching intervals must merge. That is why the code uses `<` in phase 1 and `<=` in phase 2.
- Forgetting to append the merged interval when nothing overlapped. It is appended unconditionally after phase 2, which also covers an empty list and insertion at either end.
- Updating `start` with only `intervals[i][0]` and not `min(...)`. When the new interval begins earlier, the old one must not shrink it.

## Cost

Time O(n): each interval is looked at once. Space O(n) for `result`, which holds the output.
