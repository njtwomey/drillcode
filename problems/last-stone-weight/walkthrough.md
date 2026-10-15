## The idea

Each round you need the two heaviest stones. Re-sorting after each smash costs O(n log n) per round. A heap gives the largest item in O(log n) and accepts new items in O(log n). Python's `heapq` is a min-heap, so store negated weights: the most negative number is the heaviest stone.

## Set-up

- `heap` holds `-stone` for each stone, turned into a heap by `heapq.heapify` in O(n).

Invariant: the top of `heap` (the smallest number) is the negative of the heaviest remaining stone. The loop runs while at least two stones remain.

For `[2, 7, 4, 1, 8, 1]`, drawn here by weight rather than by the negated numbers:

```text
heaviest ... lightest
  8  7  4  2  1  1
```

## Step by step

Each round pops two stones (`first` is the heavier), and pushes back `first - second` if it is not 0. The row below shows the weights in the heap after each round, listed heaviest first:

```text
start             8 7 4 2 1 1
round 1   8 vs 7  differ by 1, push 1      4 2 1 1 1
round 2   4 vs 2  differ by 2, push 2      2 1 1 1
round 3   2 vs 1  differ by 1, push 1      1 1 1
round 4   1 vs 1  equal, nothing pushed    1
```

Only one stone is left, so the loop stops and the function returns `-heap[0]`, which is 1.

## Why it works

The rule always uses the two heaviest stones, and the heap guarantees it picks exactly those. Each round removes two stones and adds at most one, so the count drops by at least one and the loop ends. The heap is always consistent because `heappush` and `heappop` repair it.

## Where it goes wrong

Forgetting the sign. Without the minus signs, `heappop` returns the lightest stone and you smash the wrong pair. And the final line has to handle an empty heap (everything cancelled):

```text
stones [3, 3]:   3 vs 3 equal, nothing pushed, heap = []
heap[0] -> IndexError, so the code returns 0 when the heap is empty
```

Push back `-(first - second)`, not `first - second`, or the heap would mix signs.

## Cost

Time O(n log n): at most n rounds, each with a few O(log n) heap operations (the initial `heapify` is O(n)). Space O(n) for the heap.
