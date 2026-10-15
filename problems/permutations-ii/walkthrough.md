## The idea

With duplicates, plain permutation search repeats itself: for `[1, 1, 2]` the two 1s are interchangeable, so swapping them yields the same sequence twice. The usual fix sorts and skips repeats. This solution avoids that by changing what a "choice" is.

At each position, choose a distinct value, not an index. If a value still has copies left, it is one option, no matter how many copies there are. Each option is tried once per position, so equal values can never create the same branch twice.

## Set-up

- `count` is a counter of how many copies of each value remain unused. For `[1, 1, 2]` it is `{1: 2, 2: 1}`.
- `path` is the permutation being built, shared and mutated.
- `result` stores finished permutations.

The invariant: `count[v]` plus the copies of `v` in `path` always equals the original number of copies.

```text
count = {1: 2, 2: 1}
path  = []
loop over the keys: 1, then 2   (a value with count 0 is skipped)
```

## Step by step

```text
path []                          count {1:2, 2:1}
├─ value 1   path [1]            count {1:1, 2:1}
│  ├─ value 1   path [1,1]       count {1:0, 2:1}
│  │  └─ value 2   path [1,1,2]  full -> save
│  └─ value 2   path [1,2]       count {1:1, 2:0}
│     └─ value 1   path [1,2,1]  full -> save
└─ value 2   path [2]            count {1:2, 2:0}
   └─ value 1   path [2,1]       count {1:1, 2:0}
      └─ value 1   path [2,1,1]  full -> save
```

Result: `[1,1,2]`, `[1,2,1]`, `[2,1,1]`: three permutations, where plain search would give six.

Note that the loop is over the counter's keys, so the value 1 appears once as a choice at the top even though there are two copies.

## Why it works

A distinct permutation is a sequence of values. At each position the tree has one branch per distinct available value, so each sequence corresponds to exactly one root-to-leaf path. Restoring `count[value] += 1` after each call keeps the counts right for the sibling branches.

## Where it goes wrong

- Looping over `nums` instead of `count`: the second 1 would start an identical branch, giving duplicates.
- Skipping `if count[value] == 0`: a value would be used more times than it exists, and paths could get longer than needed with wrong counts.
- Appending `path` rather than `path[:]`.

```text
Looping over nums = [1,1,2] at the top: tries 1, 1, 2
  the two "1" branches both produce [1,1,2] and [1,2,1]  -> repeats
```

## Cost

Worst case (all distinct) is n! results, each copied in O(n): time O(n * n!). Space beyond the output is O(n) for `count`, `path` and the recursion. With many duplicates the tree is much smaller.
