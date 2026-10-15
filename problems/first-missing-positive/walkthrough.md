## The idea

With `n` numbers, the smallest missing positive can only be in `1..n+1`. If the array contained all of `1..n`, there would be no room for anything else and the answer is `n + 1`. Otherwise something in `1..n` is absent, and the answer is the first such gap.

So the array itself can serve as a lookup table: value `v` belongs at index `v - 1`. Move every in-range value to its home slot, ignoring negatives, zeros and anything bigger than `n`. Then scan: the first index `i` where `nums[i] != i + 1` means `i + 1` is missing.

## Set-up

- `n` is the length. Only values `1..n` matter.
- The array is rearranged in place. Nothing extra is allocated, which is why it is O(1) space.
- The inner `while` loop at index `i` keeps swapping until slot `i` holds something out of range or something already sitting in its home slot.

The second test, `nums[nums[i] - 1] != nums[i]`, is what stops duplicates. If the home slot already holds the same value, swapping would do nothing and the loop would spin forever.

```text
nums = [3, 4, -1, 1]       n = 4

index:   0   1   2   3
value:   3   4  -1   1
home:    2   3   -   0      (home = value - 1)
```

## Step by step

```text
i=0  nums[0]=3 -> home index 2 holds -1, not 3.  Swap.
     [-1, 4, 3, 1]
     nums[0] = -1 is out of range, move on.

i=1  nums[1]=4 -> home index 3 holds 1, not 4.   Swap.
     [-1, 1, 3, 4]
     nums[1] = 1 -> home index 0 holds -1.       Swap.
     [1, -1, 3, 4]
     nums[1] = -1 is out of range, move on.

i=2  nums[2]=3, home index 2 already holds 3. Nothing to do.
i=3  nums[3]=4, home index 3 already holds 4. Nothing to do.
```

Final scan, looking for the first slot that does not hold `index + 1`:

```text
index:   0   1   2   3
value:   1  -1   3   4
want:    1   2   3   4
             ^ mismatch at index 1  ->  answer 2
```

## Why it works

Each swap puts at least one value into its permanent home slot, and a value in its home slot is never moved again. There are at most `n` such placements, so the total number of swaps is at most `n` even though the swapping sits in a `while` inside a `for`. After the pass every slot either holds its own `index + 1` or holds junk (out of range, or a duplicate whose home is already taken). The first slot with junk names a value that was never in the input.

If every slot is correct the input was a permutation of `1..n`, and the answer is `n + 1`.

## Where it goes wrong

- Using `nums[i], nums[nums[i] - 1] = nums[nums[i] - 1], nums[i]`. Python builds the right-hand tuple first, but the left-hand targets are assigned in order, and the second target index is computed after `nums[i]` has already changed. That is why the code stores `j = nums[i] - 1` first.
- Dropping the duplicate guard. `[1, 1]` would swap index 0 and index 0 forever.
- Not bounding the range with `n`. A value like 12 in a 5-element array has no slot.

```text
[1, 1]   i=0: nums[0]=1, home 0 holds 1.  Guard says stop.
         i=1: nums[1]=1, home 0 holds 1.  Guard says stop.
         scan: index 1 holds 1, wanted 2  ->  answer 2
```

## Other approaches

`solution_set.py` puts all values in a set and counts up from 1 until one is absent. It is simpler and leaves the input untouched, but it costs O(n) extra space, which is what the in-place version avoids.

## Cost

Time O(n): each swap fixes a value for good, so the swaps total at most `n`, plus the two linear scans. Space O(1): the array is reused as the table.
