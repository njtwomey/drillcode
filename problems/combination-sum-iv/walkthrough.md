## The idea

Despite the name, this problem counts ordered sequences: 1+2 and 2+1 are different answers. That makes it simpler than it sounds. Every sequence that sums to `t` ends in some number `n` from `nums`, and what comes before it is any sequence summing to `t - n`. So the count for `t` is the sum of the counts for `t - n` over all `n`.

## Set-up

- `dp[t]` is the number of ordered sequences of numbers from `nums` that sum to `t`.
- `dp[0] = 1`: the empty sequence makes 0. Without this, every count would be 0.
- The target loop is the outer loop and `nums` the inner. At each `t`, every number is tried as the last element, which is what distinguishes different orderings.

```text
nums = [1, 2, 3], target = 4

t      0  1  2  3  4
dp     1  0  0  0  0
```

## Step by step

```text
t=1   last = 1: dp[0] = 1                         dp[1] = 1
t=2   last = 1: dp[1] = 1,  last = 2: dp[0] = 1   dp[2] = 2
t=3   last = 1: dp[2] = 2,  last = 2: dp[1] = 1,
      last = 3: dp[0] = 1                         dp[3] = 4
t=4   last = 1: dp[3] = 4,  last = 2: dp[2] = 2,
      last = 3: dp[1] = 1                         dp[4] = 7

t      0  1  2  3  4
dp     1  1  2  4  7
```

The 7 sequences for 4, grouped by their last number:

```text
ends in 1 (dp[3] = 4):  1111  121  211  31
ends in 2 (dp[2] = 2):  112   22
ends in 3 (dp[1] = 1):  13
```

## Why it works

Every sequence summing to `t` has a unique last element, so sorting them by last element splits them into disjoint groups. Each group is in one-to-one correspondence with the sequences summing to `t - n`. Adding the groups counts every sequence once. Smaller targets are filled first, so each lookup is ready.

## Where it goes wrong

Loop order. Swapping to `nums` outer and `t` inner counts combinations (order ignored), which is Coin Change II. For `nums = [1,2,3]` and target 4 that gives 4, not 7.

```text
t outer, nums inner:   dp[4] = 7   (orderings count)
nums outer, t inner:   dp[4] = 4   (1111, 112, 22, 13)
```

Also guard with `n <= t`, or you index a negative position. A target of 0 returns 1 by `dp[0]`; an unreachable target returns 0.

## Cost

Time O(target * len(nums)). Space O(target).
