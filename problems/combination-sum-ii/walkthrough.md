## The idea

We want every distinct set of numbers from the list that adds to `target`, with each list entry used at most once. The list may contain repeats, so a naive search finds the same set several times (picking the first `2` or the second `2` gives identical results).

The fix is to sort first. Then equal values sit next to each other, and we can say: at any one decision point, only the first copy of a value may start a new branch. Later copies would only repeat the same branch. Sorting also lets us stop a loop early once a number is too big.

## Set-up

- `candidates.sort()` groups equal values and orders them by size.
- `path` is the combination being built, shared and mutated; copy it when saving.
- `backtrack(start, remaining)` means: choose the next number from `candidates[start:]` with `remaining` still to reach.
- `result` collects finished combinations.

## Step by step

Take `[2,5,2,1,2]`, `target = 5`. After sorting: `[1,2,2,2,5]`, indexes 0 to 4.

```text
backtrack(0, 5)  path []
├─ i=0 take 1 ─▶ backtrack(1, 4)  path [1]
│    ├─ i=1 take 2 ─▶ backtrack(2, 2)  path [1,2]
│    │    ├─ i=2 take 2 ─▶ backtrack(3, 0)  path [1,2,2]  SAVE
│    │    ├─ i=3 equals i-1 and i>start ─▶ skip
│    │    └─ i=4 value 5 > 2 ─▶ break
│    ├─ i=2, i=3 equal to previous, i>start ─▶ skip
│    └─ i=4 value 5 > 4 ─▶ break
├─ i=1 take 2 ─▶ backtrack(2, 3)  path [2]
│    ├─ i=2 take 2 ─▶ backtrack(3, 1)  nothing fits, break
│    ├─ i=3 skip (duplicate)
│    └─ i=4 value 5 > 3 ─▶ break
├─ i=2, i=3 skip (duplicates of the 2 just tried at this depth)
└─ i=4 take 5 ─▶ backtrack(5, 0)  path [5]  SAVE
```

Result: `[[1,2,2],[5]]`.

Notice that `[1,2,2]` still gets built even though the 2s are equal. Inside `backtrack(2, 2)` the first 2 is at `i == start`, so it is allowed.

## Why it works

Recursing on `i + 1` means each entry is used at most once. The skip rule `i > start and candidates[i] == candidates[i - 1]` keeps one representative per distinct value at each depth. Different depths can still reuse the same value (that is how `[1,2,2]` arises). The `break` is safe because the list is sorted: if one candidate exceeds `remaining`, so do all later ones.

## Where it goes wrong

Using `i > 0` instead of `i > start` for the skip. That would forbid the second 2 inside `[1,2,2]` too, since it equals its neighbour, and you would lose valid answers.

```text
wrong skip (i > 0):   [1,2] then second 2 is skipped  ─▶ [1,2,2] never built
right skip (i > start): second 2 at i == start is allowed
```

Using `continue` instead of `break` for the size check still works but wastes time on the rest of the loop.

## Cost

Time O(2^n) in the worst case, since each element is in or out. Space O(n) for the recursion depth and `path`, not counting the output.
