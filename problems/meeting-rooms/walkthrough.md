## The idea

You can attend every meeting only if no two of them overlap. The obvious check compares every pair, which is O(n^2). Sorting makes that unnecessary. Once the meetings are in order of start time, a meeting can only collide with the one right before it: if it started before some earlier meeting ended, then it also started before the meeting immediately preceding it ended, or that one would already have been flagged.

So sort once, then walk the list and compare each neighbour pair.

## Set-up

There is only one structure: `intervals`, re-bound to a sorted copy. Python sorts the `[start, end]` pairs by start first (ties broken by end), which is the order we want. The invariant for the loop is that every pair before index `i` has already been checked and is clean.

```text
intervals = [[0,30], [5,10], [15,20]]       (already sorted by start)
index:        0        1        2
```

## Step by step

For each `i` from 1, compare the start of meeting `i` with the end of meeting `i - 1`.

```text
i = 1   previous = [0,30]   current = [5,10]

   0                              30
   |==============================|        previous
        5     10
        |=====|                           current starts at 5 < 30
                                           ──▶ overlap, return False
```

That ends early. Now a case that passes, `[[5,8],[1,5]]`. After sorting it is `[[1,5],[5,8]]`:

```text
i = 1   previous = [1,5]   current = [5,8]

   1     5
   |=====|                  previous
         5     8
         |=====|            current starts at 5, and 5 < 5 is False
                            ──▶ no conflict, loop ends, return True
```

## Why it works

After sorting, start times never decrease. For meeting `i` to clash with any earlier meeting `j`, it must start before `j` ends. That is only a problem if `j` really runs past the start of `i`, and the strict check on neighbours catches the first such clash while walking the list. Any clash involving a far-away earlier meeting implies a clash with an adjacent one, because the meetings in between start no later than `i`. An empty list or a single meeting has no pairs, so the loop never runs and the answer is `True`.

## Where it goes wrong

The comparison must be strict. Back-to-back meetings share an endpoint but do not overlap, so `<=` would reject them.

```text
[1,5] then [5,8]
   wrong:  5 <= 5  ──▶ False   (but you can walk straight from one to the next)
   right:  5 <  5  ──▶ no conflict
```

Forgetting to sort is the other trap: neighbours in unsorted order are meaningless. `[[7,10],[2,4]]` is fine to attend (the meetings are disjoint), but the unsorted check sees `2 < 10` and wrongly returns `False`.

## Cost

Time O(n log n), dominated by the sort; the scan is O(n). Space O(n) for the sorted copy that `sorted` makes, though the scan itself needs only a few integers.
