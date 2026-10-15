## The idea

With duplicate values, the plain subset enumeration produces repeats: from `[1, 2, 2]`, choosing "the first 2" and choosing "the second 2" both give `[1, 2]`. We need each distinct subset once.

Sort first so equal values sit next to each other. Then build subsets by backtracking over start indices: a subset grows by picking, in order, elements from later positions. The rule that kills duplicates is simple. At one level of the recursion, never pick a value that is equal to the one just before it in the loop, because that earlier pick already explored every subset the later copy would build.

## Set-up

- `nums.sort()` groups duplicates.
- `result` holds the finished subsets. `path` is the subset being built.
- `backtrack(start)` records the current `path` (every path is a valid subset the moment it exists), then tries each `i` from `start` onward as the next element.
- Invariant: `path` only ever uses indices in increasing order, so each combination of positions is reached once.

```text
nums sorted = [1, 2, 2]        indices 0  1  2
```

## Step by step

A skip happens when `i > start` and `nums[i] == nums[i - 1]`.

```text
backtrack(0)        path=[]            record []
  i=0  take 1
  backtrack(1)      path=[1]           record [1]
    i=1  take 2
    backtrack(2)    path=[1,2]         record [1,2]
      i=2  take 2   (i == start, allowed)
      backtrack(3)  path=[1,2,2]       record [1,2,2]
    i=2  2 == 2 and i > start: SKIP    (would repeat [1,2])
  i=1  take 2
  backtrack(2)      path=[2]           record [2]
    i=2  take 2     (i == start, allowed)
    backtrack(3)    path=[2,2]         record [2,2]
  i=2  2 == 2 and i > start: SKIP      (would repeat [2])
```

The result is `[], [1], [1,2], [1,2,2], [2], [2,2]`: six subsets, no repeats.

## Why it works

Among equal values, the rule forces a fixed order: the second copy may only be chosen after the first copy has been chosen on the same path. At the point where the loop reaches a repeat of the previous value, the first copy was a choice that had already been tried at this depth, and everything the second copy could lead to is a repeat of what the first copy led to. Deeper in the recursion, a copy is the first element at its depth (`i == start`), so it is allowed, which is how `[2, 2]` is still found.

## Where it goes wrong

The condition must be `i > start`, not `i > 0`. With `i > 0` the second 2 would be skipped even at depth 2, so `[1, 2, 2]` and `[2, 2]` disappear.

```text
path=[1,2], start=2, i=2:  nums[2]==nums[1]
  correct test i > start: 2 > 2 false -> allowed -> [1,2,2]
  wrong   test i > 0     :           -> skipped, subset lost
```

Skipping the sort breaks it too, since equal values would not be neighbours. Also copy `path` (`path[:]`) before storing it, as it keeps changing.

## Cost

Time O(n · 2^n) in the worst case (all distinct): each subset is copied once. Space O(n) for `path` and the recursion, beyond the output.
