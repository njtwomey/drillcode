## The idea

For each job you either skip it or take it. Taking it means the other chosen jobs must all finish by its start time. If the jobs are sorted by end time, "all jobs that finish by this start" is a prefix of the list, so the best profit over that prefix is a single stored number. That turns an apparent search over subsets into a one-pass DP with a binary search.

Brute force tries every subset, which is exponential. Sorting by end time is what makes the compatible earlier jobs form a contiguous block.

## Set-up

- `jobs` is `sorted(zip(endTime, startTime, profit))`, so jobs are in end-time order.
- `best[k]` is the maximum profit using only the first `k` jobs in that order. `best[0] = 0` for no jobs.
- `ends` holds the end times of the jobs already processed, ascending, so we can binary search it.

```text
startTime = [1, 2, 3, 3]
endTime   = [3, 4, 5, 6]
profit    = [50, 10, 40, 70]

sorted by end:   (end, start, gain)
  job 1: (3, 1, 50)
  job 2: (4, 2, 10)
  job 3: (5, 3, 40)
  job 4: (6, 3, 70)

best = [0]      ends = []
```

## Step by step

For each job, `k = bisect_right(ends, start)` counts the earlier jobs ending at or before this start. Then `best[-1]` (skip) competes with `best[k] + gain` (take it on top of the best schedule of those `k` jobs).

```text
job (3,1,50)  k = 0   skip: 0     take: best[0]+50 = 50   -> 50
              best = [0, 50]          ends = [3]

job (4,2,10)  k = 0   skip: 50    take: best[0]+10 = 10   -> 50
              best = [0, 50, 50]      ends = [3, 4]

job (5,3,40)  k = 1   ends <= 3: just the first job
              skip: 50    take: best[1]+40 = 90   -> 90
              best = [0, 50, 50, 90]  ends = [3, 4, 5]

job (6,3,70)  k = 1   skip: 90    take: best[1]+70 = 120  -> 120
              best = [0, 50, 50, 90, 120]
```

The answer is `best[-1] = 120`: the first job (1 to 3) and the last (3 to 6).

## Why it works

`best[k]` really is the optimum for the first `k` jobs: the optimal schedule for the first `k` either leaves job `k` out (then it is `best[k-1]`) or includes it. If it includes job `k`, every other chosen job ends by job `k`'s start, so those are among the first `k'` jobs, where `k'` is the bisect result, and the best of those is `best[k']`. Taking the larger of the two covers every case.

## Where it goes wrong

Using `bisect_left` instead of `bisect_right`. A job may start exactly when another ends, so ends equal to `start` must count as compatible.

```text
ends = [3, 4]   start = 4

bisect_right -> 2   (the job ending at 4 is allowed)
bisect_left  -> 1   (it is wrongly excluded)
```

Also, `ends` is a separate list of end times because `bisect` needs a plain sorted list to search.

## Cost

Time O(n log n): the sort, then one binary search per job. Space O(n) for `jobs`, `best` and `ends`.
