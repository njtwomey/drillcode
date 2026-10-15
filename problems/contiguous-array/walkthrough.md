## The idea

We want the longest stretch with the same number of 0s and 1s. Checking every start and end pair is O(n^2).

Make it a sum problem: count each `1` as `+1` and each `0` as `-1`. A stretch has equal 0s and 1s exactly when its values sum to zero. Keep a running `balance`. If the balance is the same at two positions, everything between them sums to zero, so that stretch is balanced. The longest balanced stretch comes from the two furthest-apart equal balances.

## Set-up

- `balance` is the running total so far (ones minus zeros).
- `first_seen` maps each balance to the earliest index where it appeared. It starts as `{0: -1}`: before the array begins (index -1) the balance is 0. This lets a stretch that starts at index 0 be measured.
- `best` is the longest length found.

Only the first index of each balance is stored. A later equal balance always forms a longer stretch with the earliest one.

## Step by step

`nums = [0,1,1,1,1,1,0,0,0]`:

```text
i        -1   0   1   2   3   4   5   6   7   8
num           0   1   1   1   1   1   0   0   0
balance   0  -1   0   1   2   3   4   3   2   1
```

Walk through the indexes:

```text
i=0  balance -1 new         first_seen {0:-1, -1:0}
i=1  balance  0 seen at -1  length 1-(-1) = 2    best = 2
i=2  balance  1 new         first_seen adds 1:2
i=3  balance  2 new         adds 2:3
i=4  balance  3 new         adds 3:4
i=5  balance  4 new         adds 4:5
i=6  balance  3 seen at 4   length 6-4 = 2       best = 2
i=7  balance  2 seen at 3   length 7-3 = 4       best = 4
i=8  balance  1 seen at 2   length 8-2 = 6       best = 6
```

The answer is 6: indexes 3 to 8, which are `1,1,1,0,0,0`.

```text
index    0  1  2 │ 3  4  5  6  7  8
num      0  1  1 │ 1  1  1  0  0  0
                   └─── 6 long ───┘
```

## Why it works

The balance after index `j` minus the balance after index `i` is the sum of the stretch `i+1..j`. If those balances are equal, the sum is zero. By remembering the first index per balance, each `j` is paired with the farthest possible `i`.

## Where it goes wrong

Leaving out `{0: -1}`. With `[0,1]` the balance returns to 0 at index 1, and with no entry for 0 the stretch from the very start is never counted (answer would be 0 instead of 2).

Overwriting `first_seen[balance]` on every visit is the other slip: it keeps the latest index and shrinks every stretch.

## Cost

Time O(n): one pass with O(1) dictionary work. Space O(n) for `first_seen`.
