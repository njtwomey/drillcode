## The idea

A subarray sum is `prefix[j] - prefix[i]` for two prefix sums. That difference is divisible by `k` exactly when the two prefixes leave the same remainder mod `k`. So instead of tracking sums, track remainders and count pairs of prefixes that share one. No pair of loops is needed, only a tally by remainder.

## Set-up

- `count_of` maps a remainder to how many prefixes so far had it. It starts as `{0: 1}`, the empty prefix, so subarrays that start at index 0 are counted.
- `prefix` holds the current prefix sum already reduced mod `k`. Reducing at each step keeps it small and does not change any remainder.
- `result` is the running count.

```text
nums = [4, 5, 0, -2, -3, 1]     k = 5

count_of = {0: 1}    prefix = 0     result = 0
```

## Step by step

For each number: `prefix = (prefix + num) % k`, add `count_of[prefix]` to `result` (each earlier prefix with that remainder pairs with this one), then bump `count_of[prefix]`.

```text
num    prefix  pairs found  result  count_of after
 4       4        0           0     {0:1, 4:1}
 5       4        1           1     {0:1, 4:2}        subarray [5]
 0       4        2           3     {0:1, 4:3}        [0], [5,0]
-2       2        0           3     {0:1, 4:3, 2:1}
-3       4        3           6     {0:1, 4:4, 2:1}   ends at -3
 1       0        1           7     {0:2, 4:4, 2:1}   whole array
```

Seven subarrays have a sum that is a multiple of 5. At the fifth step, `-3` makes the prefix return to remainder 4, which matches three earlier prefixes, so three subarrays end there.

## Why it works

Two prefixes with equal remainders differ by a multiple of `k`, and that difference is the sum of the subarray between them. Every valid subarray corresponds to exactly one such pair, with the right end being the current element. Counting the earlier matches at each right end therefore counts each subarray once.

## Where it goes wrong

- Forgetting the seed `{0: 1}`. Subarrays that begin at index 0 pair with the empty prefix and would be lost.
- Negative prefixes in languages whose `%` can go negative. Python's `%` returns a value in `[0, k)`, so `-1` and `k - 1` fall in the same bucket.

```text
k = 5,  prefix sums 4 and -1 are the same remainder class
Python:   4 % 5 = 4     -1 % 5 = 4    -> same bucket, pair found
C++/Java: 4 % 5 = 4     -1 % 5 = -1   -> different buckets, pair missed
```

## Cost

Time O(n): one pass. Space O(k): at most `k` distinct remainders.
