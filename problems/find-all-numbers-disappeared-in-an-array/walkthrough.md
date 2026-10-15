## The idea

The list has `n` numbers, each between 1 and `n`. Some appear twice, so others are missing. We want the missing ones without a second list.

The values are valid indices (value `v` belongs at index `v - 1`), so the array can act as its own record of what has been seen. When you meet value `v`, mark slot `v - 1` by making it negative. After one pass, any slot that is still positive was never pointed at, so its number is missing.

## Set-up

There are no new variables beyond the loop. The array `nums` is the seen-set:

- A negative entry at index `i` means "the value `i + 1` is present".
- The magnitude of each entry is still the original number, so we can read it with `abs()`.

Invariant: during the loop, `abs(nums[j])` is the original value at `j`, and the sign of `nums[j]` records whether `j + 1` has been met.

## Step by step

Input `[4, 3, 2, 7, 8, 2, 3, 1]`, so `n = 8`. Each row shows the value read, the slot marked, and the array afterwards:

```text
read   slot   array after
 4      3     [ 4,  3,  2, -7,  8,  2,  3,  1]
 3      2     [ 4,  3, -2, -7,  8,  2,  3,  1]
-2->2   1     [ 4, -3, -2, -7,  8,  2,  3,  1]   (nums[2] was already -2)
-7->7   6     [ 4, -3, -2, -7,  8,  2, -3,  1]
 8      7     [ 4, -3, -2, -7,  8,  2, -3, -1]
 2      1     [ 4, -3, -2, -7,  8,  2, -3, -1]   (already negative, stays)
-3->3   2     [ 4, -3, -2, -7,  8,  2, -3, -1]   (already negative, stays)
-1->1   0     [-4, -3, -2, -7,  8,  2, -3, -1]
```

Still positive: indices 4 and 5, so the missing numbers are `5` and `6`.

```text
index:  0   1   2   3   4   5   6   7
array: -4  -3  -2  -7   8   2  -3  -1
                        ^   ^
                      5 and 6 never marked
```

## Why it works

Each present value `v` forces slot `v - 1` negative, and nothing else touches that sign. A slot stays positive only if no element equals its number. Repeats do no harm because marking is idempotent.

## Where it goes wrong

Two details. First, read through `abs(num)`: by the time you reach an element it may already be negative, and a negative index would point at the wrong slot (counting from the end).

Second, write `-abs(nums[index])`, not `-nums[index]`. Negating blindly flips the sign back on the second visit:

```text
value 2 seen twice, slot 1 holds 3
first:  -3   marked
second: +3   WRONG, looks unmarked again
```

## Other approaches

`solution_set.py` builds `set(nums)` and lists each `v` in `1..n` not in it. Same O(n) time, but the set costs O(n) space. The sign trick removes that, at the price of modifying the input.

## Cost

Time O(n): one marking pass and one collecting pass. Space O(1) beyond the output list.
