## The idea

The slow way is to scan every interval for every query. With 100,000 of each, that is far too much work.

The fix is to stop answering queries in the order they arrive. If you answer them from smallest to largest, the set of intervals that could matter changes in a simple way: an interval becomes a candidate once the query reaches its left end, and it stops being a candidate once the query passes its right end. Intervals enter once and leave once. Among the current candidates you always want the smallest size, which is exactly what a min-heap is for.

The answers are written back at each query's original position, so the caller still sees them in input order.

## Set-up

- `intervals.sort()` orders intervals by left end, so `i` can walk through them once.
- `i` is the next interval that has not been admitted yet. Everything before `i` starts at or before the current query.
- `heap` holds `(size, end)` for admitted intervals. Size comes first so the smallest interval is on top.
- `result` starts as all `-1`, which is the answer for a query nothing covers.
- `sorted((q, idx) ...)` gives the queries in increasing order while remembering where each came from.

```text
intervals (sorted)   [1,4] [2,4] [3,6] [4,4]
                       ^ i
queries (value,idx)  (2,0) (3,1) (4,2) (5,3)
heap                 empty
result               [-1, -1, -1, -1]
```

## Step by step

Each heap entry is `(size, end)`. The example is the first test: intervals `[1,4] [2,4] [3,6] [4,4]`, queries `2 3 4 5`.

```text
q = 2   admit starts <= 2:  [1,4] -> (4,4)   [2,4] -> (3,4)
        heap (top first): (3,4) (4,4)
        top end 4 >= 2, still valid.          result[0] = 3

q = 3   admit [3,6] -> (4,6)
        heap: (3,4) (4,4) (4,6)
        top end 4 >= 3.                       result[1] = 3

q = 4   admit [4,4] -> (1,4)
        heap: (1,4) (3,4) (4,4) (4,6)
        top end 4 >= 4.                       result[2] = 1

q = 5   nothing left to admit
        heap: (1,4) (3,4) (4,4) (4,6)
        pop (1,4): end 4 < 5
        pop (3,4): end 4 < 5
        pop (4,4): end 4 < 5
        top is now (4,6), end 6 >= 5.         result[3] = 4
```

Final `result` is `[3, 3, 1, 4]`.

## Why it works

Every entry in the heap started at or before the current query, so the only thing that can disqualify it is having ended already. The loop that pops the top while its `end < q` removes those. Because queries only grow, an expired interval is expired for every later query, so removing it is permanent.

You do not need to clean the whole heap. An expired interval buried below the top cannot be the answer, because the top is checked before it is used. It gets removed whenever it surfaces. After cleaning, the top is the smallest-size interval that started and has not ended, which is the answer.

## Where it goes wrong

- Skipping the original index. Sorting queries scrambles their order, so each answer must go to `result[idx]`.
- Checking `heap[0][1] < q` only once instead of in a loop. Several tops can be expired in a row, as in the `q = 5` step above.
- Comparing with `<=` for the end. Both ends are inclusive, so an interval ending exactly at `q` is still valid.

## Cost

Time O((n + q) log(n + q)): two sorts, plus each interval is pushed once and popped at most once. Space O(n + q) for the heap, the result and the sorted query list.
