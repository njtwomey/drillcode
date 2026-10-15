## The idea

You need the number of 1 bits for every number from 0 to `n`. Counting each one separately costs O(n log n). But every number is a smaller number with one extra bit stuck on the end, and the smaller number's answer is already in the table. Shifting right drops the last bit; that last bit adds 1 if it was set.

So `dp[i] = dp[i >> 1] + (i & 1)`.

## Set-up

- `dp` has `n + 1` slots, all 0. `dp[0] = 0` is the base case: zero has no set bits.

Invariant: when the loop reaches `i`, every slot below `i` is correct. `i >> 1` is always less than `i` (for `i >= 1`), so the slot we read is ready.

## Step by step

For `n = 5`, with binary shown so the idea is visible:

```text
 i   binary   i>>1   i&1   dp[i>>1] + (i&1)   dp[i]
 1    001      0      1      0 + 1               1
 2    010      1      0      1 + 0               1
 3    011      1      1      1 + 1               2
 4    100      2      0      1 + 0               1
 5    101      2      1      1 + 1               2
```

Result: `[0, 1, 1, 2, 1, 2]`.

Take `i = 5`: `101` is `10` (the number 2, which has one bit) followed by a trailing `1`, so 1 + 1 = 2.

## Why it works

Writing `i` in binary, its bits are the bits of `i >> 1` plus the final bit `i & 1`. Counting ones is additive over that split, so the recurrence is exact.

## Where it goes wrong

Filling in the wrong order. The table must go from small to large, otherwise `dp[i >> 1]` is still 0. Also keep `dp[0] = 0` and start the loop at 1; the formula would still give 0 at `i = 0`, but there is no point.

Do not confuse `i & 1` (the last bit) with `i & (i - 1)` (which clears the lowest set bit, a different recurrence).

```text
i = 6 = 110      i & 1 = 0       i >> 1 = 3 = 11
dp[6] = dp[3] + 0 = 2
```

## Other approaches

`countBitsLowbit` uses `dp[i] = dp[i & (i - 1)] + 1`. The expression `i & (i - 1)` erases the lowest set bit, leaving a smaller number with exactly one fewer 1:

```text
i = 6    110
i-1 = 5  101
i&(i-1)  100  = 4     dp[6] = dp[4] + 1 = 2
```

## Cost

Time O(n), each entry is a constant number of operations. Space O(n) for the table that is returned.
