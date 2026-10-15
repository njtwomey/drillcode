## The idea

We need all the zeros at the back, the non-zeros in their original order, and no second array. Think of it as compacting: collect the non-zeros at the front, and whatever is left over is zeros.

Two indices do it. `read` scans every element. `write` marks the next slot where a non-zero belongs. When `read` finds a non-zero, swap it into the `write` slot and advance `write`. The zeros it skipped over get pushed backwards by those swaps.

## Set-up

- `write` starts at 0: the front slot waiting for the next non-zero.
- `read` is the loop index, scanning left to right.

Invariant: `nums[:write]` holds the non-zeros seen so far, in original order, and everything from `write` up to `read` is zero.

```text
nums = [0, 1, 0, 3, 12]
         ^
         write, read
```

## Step by step

```text
read=0  value 0: skip.
        [0, 1, 0, 3, 12]
         ^w,r

read=1  value 1: swap nums[0] and nums[1], write becomes 1.
        [1, 0, 0, 3, 12]
            ^w,r

read=2  value 0: skip.
        [1, 0, 0, 3, 12]
            ^w ^r

read=3  value 3: swap nums[1] and nums[3], write becomes 2.
        [1, 3, 0, 0, 12]
               ^w ^r

read=4  value 12: swap nums[2] and nums[4], write becomes 3.
        [1, 3, 12, 0, 0]
                   ^w (read has reached the end)
```

Final array: `[1, 3, 12, 0, 0]`. The non-zeros kept their relative order, and each swap dropped a zero from the `write` slot into the place the non-zero came from.

## Why it works

Between `write` and `read` there are only zeros. When `read` meets a non-zero, swapping it with `nums[write]` (a zero, or itself) puts it in the right place and moves that zero to `read`, which is behind the scan, so the invariant holds. Skipped zeros therefore drift right as non-zeros move left. Since `read` only moves forward, original order among non-zeros is preserved.

## Where it goes wrong

If there are no zeros before a non-zero, `write == read` and the swap is a self-swap, which is harmless. Do not guard against it; it is cheaper than a branch. The real trap is copying instead of swapping and forgetting to fill the tail with zeros:

```text
copy only:  [0, 1, 0, 3, 12]  ──▶  [1, 3, 12, 3, 12]   tail not zeroed
swap:                          ──▶  [1, 3, 12, 0, 0]
```

## Cost

Time O(n), one pass with at most n swaps. Space O(1), two indices, in place.
