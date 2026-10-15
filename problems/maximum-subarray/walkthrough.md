## The idea

Trying every subarray is O(n²). Kadane's algorithm uses one observation: the best subarray ending at position `i` either starts fresh at `nums[i]`, or extends the best subarray ending at `i - 1`. If the running sum before `i` is negative, carrying it forward only hurts, so we drop it and start over.

## Set-up

- `cur` is the best sum of a subarray that ends at the current element. It starts as `nums[0]`.
- `best` is the largest `cur` seen so far. It also starts as `nums[0]`.
- Invariant: `cur` is always the sum of a real, non-empty subarray ending here.

## Step by step

`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`. Each round sets `cur = max(num, cur + num)`.

```text
 num   cur + num   cur = max(num, cur+num)   best
 -2        -        -2                       -2     start
  1       -1         1  (restart)             1
 -3       -2        -2  (restart)             1
  4        2         4  (restart)             4
 -1        3         3  (extend)              4
  2        5         5  (extend)              5
  1        6         6  (extend)              6
 -5        1         1  (extend)              6
  4        5         5  (extend)              6
```

The answer is 6, from the subarray `4, -1, 2, 1`. The restart at `4` is where the running sum `-2` stopped being worth carrying.

```text
index   0   1   2   3   4   5   6   7   8
nums   -2   1  -3   4  -1   2   1  -5   4
                     └───────────┘
                       sum = 6
```

## Why it works

Every subarray ends somewhere, and `cur` is the best one ending at each index. The overall answer is the best over all ending positions, which is `best`. Extending a negative prefix never beats starting fresh, so `max(num, cur + num)` is exactly the right choice.

## Where it goes wrong

Initialising `best` and `cur` to 0 breaks all-negative input. For `[-3, -1]` the answer must be `-1` (a subarray cannot be empty), but a zero start would return 0. Starting from `nums[0]` and looping over `nums[1:]` avoids this.

## Cost

Time O(n), space O(1). The divide-and-conquer follow-up is O(n log n) and mostly worth knowing as an exercise.
