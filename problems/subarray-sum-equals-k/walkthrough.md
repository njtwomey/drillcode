## The idea

Counting subarrays whose sum is `k` looks like it needs two nested loops, one for the start and one for the end. The way out is the prefix sum. Let `prefix[i]` be the sum of the first `i` numbers. The subarray from `j` to `i - 1` sums to `prefix[i] - prefix[j]`. So a subarray ending here has sum `k` exactly when an earlier prefix equals `prefix - k`.

That turns the inner loop into a lookup. Keep a tally of how many times each prefix value has appeared, and at each step add the tally of `prefix - k`.

A sliding window would be the first idea, but it fails: negative numbers and zeros mean that growing the window does not always grow the sum.

## Set-up

- `count_of` maps a prefix value to how many earlier prefixes had it. It starts as `{0: 1}`, the empty prefix, so subarrays that start at index 0 are found.
- `prefix` is the running sum so far, starting at 0.
- `result` is the count of matching subarrays.

```text
nums = [1, 2, 3]     k = 3

count_of = {0: 1}    prefix = 0     result = 0
```

## Step by step

For each number: add it to `prefix`, add `count_of[prefix - k]` to `result`, then record `prefix`.

```text
num=1   prefix=1   look up 1-3 = -2  -> 0       result = 0
        count_of = {0:1, 1:1}

num=2   prefix=3   look up 3-3 =  0  -> 1       result = 1   ([1, 2])
        count_of = {0:1, 1:1, 3:1}

num=3   prefix=6   look up 6-3 =  3  -> 1       result = 2   ([3])
        count_of = {0:1, 1:1, 3:1, 6:1}
```

The two hits are `[1, 2]` (prefix 3 minus the empty prefix 0) and `[3]` (prefix 6 minus prefix 3).

## Why it works

Every subarray is identified by the pair of prefixes at its two ends, and it sums to `k` when they differ by `k`. By scanning left to right, each step counts every valid left end for the current right end. Prefix values can repeat (zeros, negatives), and each earlier occurrence is a different subarray, which is why the tally stores a count and not just "seen".

## Where it goes wrong

- Leaving out `{0: 1}`. Then `[1, 2]` above is missed, because its left end is the empty prefix.
- Recording the current prefix before the lookup. With `k = 0` the current prefix would match itself and count an empty subarray.

```text
nums = [5], k = 0
right: look up 5 - 0 = 5 -> 0, then record 5.   result 0
wrong: record 5 first, then look up 5 -> 1.     result 1 (empty subarray)
```

## Cost

Time O(n): one pass with O(1) dictionary operations. Space O(n) for `count_of` when all prefix sums differ.
