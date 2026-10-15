## The idea

Sorting makes consecutive runs obvious, but sorting is O(n log n). We can do better with a hash set, which answers "is this number present?" in constant time. The only extra insight is to avoid redundant work: count a run only from its smallest number. A number whose predecessor `num - 1` exists is in the middle of some run, so skip it, because that run will be counted from its start.

## Set-up

- `values = set(nums)` gives O(1) membership checks and removes duplicates, which would otherwise be double counted.
- `best` is the longest run length found so far, starting at 0 (an empty input gives 0).
- For each run start, `length` counts how far the run extends upward.

```text
nums = [100, 4, 200, 1, 3, 2]
values = {1, 2, 3, 4, 100, 200}

run starts are the numbers with no predecessor in the set:  1, 100, 200
```

## Step by step

We look at each value once, in whatever order the set yields them. Order does not matter.

```text
num=100   99 in set? no  -> start. length=1, 101 in set? no     -> run of 1
num=200  199 in set? no  -> start. length=1, 201 in set? no     -> run of 1
num=4      3 in set? yes -> skip (middle of a run)
num=3      2 in set? yes -> skip
num=2      1 in set? yes -> skip
num=1      0 in set? no  -> start.
                length=1: 1+1=2 in set -> length=2
                          1+2=3 in set -> length=3
                          1+3=4 in set -> length=4
                          1+4=5 in set? no, stop             -> run of 4
best = max(1, 1, 4) = 4
```

```text
number line:    1  2  3  4 ........ 100 ........ 200
                ├──run of 4──┤       └ 1 ┘        └ 1 ┘
```

## Why it works

Every run has exactly one smallest element, the only one without a predecessor, so each run is counted once from its start. Walking up through consecutive members measures its true length. Skipping non-starts is also what keeps it linear: the inner `while` loops together touch each element at most once across all runs.

## Where it goes wrong

- Dropping the `num - 1 not in values` test. The algorithm still gives the right answer but becomes O(n^2) on input like `1..n`, where each number walks the rest of its run.
- Iterating over `nums` with duplicates. The code iterates over the set, so `[1, 0, 1, 2]` is the run `0, 1, 2`, length 3, not 4.
- Empty input: `best` stays 0, which is correct.
- Negative numbers need no special handling.

## Cost

Time O(n): building the set is linear, and each element is visited by the outer loop once and by at most one inner walk. Space O(n) for the set.
