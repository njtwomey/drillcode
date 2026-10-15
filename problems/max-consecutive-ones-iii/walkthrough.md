## The idea

Flipping up to `k` zeros to get the longest run of ones is the same as finding the longest window that contains at most `k` zeros. The zeros inside the window are the ones you would flip. You never flip anything; you only count.

Brute force tries every window, which is O(n²). A sliding window sees each element enter and leave once.

## Set-up

- `left` is the start of the window; `right` (the loop index) is the end.
- `zeros` is the number of zeros inside the window.
- `best` is the longest valid window so far.
- Invariant: after the inner `while`, `zeros <= k`.

## Step by step

`nums = [1, 0, 0, 1, 1, 0, 1]`, `k = 1`. Brackets mark the window after the round.

Each row shows the window after the round.

```text
 r   num  zeros(after)  left  window        len  best
 0   1    0             0     [1]           1    1
 1   0    1             0     [1 0]         2    2
 2   0    1             2     [0]           1    2
 3   1    1             2     [0 1]         2    2
 4   1    1             2     [0 1 1]       3    3
 5   0    1             3     [1 1 0]       3    3
 6   1    1             3     [1 1 0 1]     4    4
```

At `r=2` the zeros reached 2, so `left` advanced past index 0 (a one, nothing changes) and then past index 1 (a zero, `zeros` drops back to 1). At `r=5` another zero arrives, and `left` moves past the zero at index 2.

The answer is 4: the window `1 1 0 1` becomes four ones with one flip.

## Why it works

For each `right`, the loop moves `left` the minimum distance to make the window legal, so the window is the longest legal one ending at `right`. Taking the maximum over all `right` covers every possible answer.

## Where it goes wrong

Use `while`, not `if`. Moving `left` once might remove a one, leaving `zeros` still above `k`; the window would be invalid when measured. With `k = 0` the window must shrink past a whole run of ones to drop the offending zero, which is exactly what the loop does.

## Cost

Time O(n): each of `left` and `right` moves at most n times. Space O(1).
