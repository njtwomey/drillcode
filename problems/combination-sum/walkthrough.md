## The idea

We want every set of numbers, each reusable any number of times, that adds to `target`. The shape of the search is a decision tree: at each step, pick the next number to add. Left alone this would produce [2,3] and [3,2] as separate answers.

Two rules prevent that waste. Only ever pick candidates at the current index or later (never go back), so each combination is built in one fixed order. And because the list is sorted, as soon as one candidate is larger than what is left, every later candidate is too, so stop the loop.

## Set-up

- `candidates` is sorted, so a too-big number means all later ones are too big.
- `path` is the combination being built. It is shared, so we copy it when we save one.
- `dfs(start, remaining)` picks the next number from `candidates[start:]`, with `remaining` left to reach.
- `remaining == 0` means `path` is a full answer. Save a copy and return.

## Step by step

`candidates = [2,3,6,7]`, `target = 7`:

```text
dfs(0, 7)  path []
├─ take 2 ─▶ dfs(0, 5)  path [2]
│   ├─ take 2 ─▶ dfs(0, 3)  path [2,2]
│   │   ├─ take 2 ─▶ dfs(0, 1)  path [2,2,2]
│   │   │             2 > 1 ─▶ break
│   │   ├─ take 3 ─▶ dfs(1, 0)  path [2,2,3]  SAVE
│   │   └─ 6 > 3 ─▶ break
│   ├─ take 3 ─▶ dfs(1, 2)  path [2,3]
│   │             3 > 2 ─▶ break
│   └─ 6 > 5 ─▶ break
├─ take 3 ─▶ dfs(1, 4)  path [3]
│   ├─ take 3 ─▶ dfs(1, 1)  3 > 1 ─▶ break
│   └─ 6 > 4 ─▶ break
├─ take 6 ─▶ dfs(2, 1)  6 > 1 ─▶ break
└─ take 7 ─▶ dfs(3, 0)  path [7]  SAVE
```

Result: `[[2,2,3],[7]]`.

## Why it works

Because the recursion always passes down an index `>=` the one just used, every combination is generated in non-decreasing order, once. Passing `i` (not `i + 1`) is what allows the same number to be reused. Any valid combination, written in sorted order, is one path in the tree, so none are missed. The `path.pop()` after each call puts the shared list back as it was.

## Where it goes wrong

Two slips:

- Passing `i + 1` instead of `i` would forbid reuse, so `[2,2,3]` would never appear.
- Restarting the loop at 0 inside the recursion makes order matter:

```text
start = 0 each time:   [2,3,2], [3,2,2], [2,2,3] ... all counted
start = i:             only [2,2,3]
```

Saving `path` without copying leaves the result full of references to one list that ends up empty.

A target smaller than every candidate saves nothing and returns `[]`.

## Cost

Time roughly O(N^(T/M)), where T is the target and M the smallest candidate: the tree is at most T/M deep and branches up to N ways. Space O(T/M) for the recursion and `path`, excluding output.
