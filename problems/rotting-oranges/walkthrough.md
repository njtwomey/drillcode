## The idea

Rot spreads one step in every direction each minute, from all rotten oranges at the same time. That is a breadth-first search where each BFS level is one minute. The one thing to get right is that the search must start from every rotten orange together. If you ran a separate search from each, you would measure how long each takes alone and not how fast they work in parallel.

## Set-up

- `queue` holds the rotten oranges whose neighbours have not been spread to yet. It is seeded with every `2` in the grid.
- `fresh` counts the fresh oranges. It tells us when we are done and whether any were unreachable.
- `minutes` counts the levels processed.

The invariant: at the start of each minute, `queue` holds exactly the oranges that rotted last minute (or at the start).

```text
grid        2 1 1       queue = [(0,0)]
            1 1 0       fresh = 6
            0 1 1       minutes = 0
```

## Step by step

Each minute handles exactly `len(queue)` oranges, the current level. A fresh neighbour is turned to `2` the moment it is queued, so it cannot be queued twice.

```text
start        minute 1     minute 2     minute 3     minute 4
2 1 1        2 2 1        2 2 2        2 2 2        2 2 2
1 1 0        2 1 0        2 2 0        2 2 0        2 2 0
0 1 1        0 1 1        0 1 1        0 2 1        0 2 2

queue        (1,0)(0,1)   (1,1)(0,2)   (2,1)        (2,2)
after        fresh = 4    fresh = 2    fresh = 1    fresh = 0
```

In minute 2, `(1,0)` rots `(1,1)` first, so when `(0,1)` also touches it, it is already rotten. In minute 3, `(0,2)` has no fresh neighbour: `(1,2)` is empty.

`fresh` reaches 0 during minute 4, the loop stops, and the answer is `4`.

## Why it works

BFS reaches each cell in the fewest steps from the nearest source, and processing the queue a whole level at a time keeps the steps in sync with the minutes. The loop ends when `fresh` hits 0, so the minute count is the time the last fresh orange rotted. If the queue empties while `fresh > 0`, the remaining oranges are walled off by empty cells, so the answer is `-1`.

## Where it goes wrong

- Counting a final empty level. If the loop were `while queue`, the last oranges to rot would be queued, then one more empty-handed minute would be counted, and the answer would be 5. The extra `and fresh` guard prevents that.
- Marking oranges as rotten when they are popped rather than when pushed. Two neighbours could queue the same orange, and `fresh` would be decremented twice.

```text
(1,0) and (0,1) both touch (1,1). Mark on push: (1,1) queued once.
Mark on pop:  (1,1) queued twice, fresh over-counted.
```

- No fresh oranges to begin with. The loop does not run, `fresh` is 0, and the answer is 0.

## Cost

Time O(m * n): each cell is queued at most once and checked from four neighbours. Space O(m * n) for the queue in the worst case. The grid is modified in place.
