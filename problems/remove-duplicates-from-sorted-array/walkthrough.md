## The idea

In a sorted array, equal values sit next to each other. So a value is a duplicate exactly when it equals the last unique value we kept. That means we can build the deduplicated array inside the same array: scan once, and copy a value forward only when it is new.

The answer the task wants is the number of unique values, and the first that many slots hold them in order. What sits after that does not matter.

## Set-up

- `write` is the next slot to fill, and also how many unique values have been kept so far. It starts at 1 because `nums[0]` is always unique.
- `read` scans from index 1 to the end.

Invariant: `nums[:write]` holds the distinct values seen so far, in sorted order, and `nums[write - 1]` is the last of them.

```text
nums = [0, 0, 1, 1, 1, 2]
         ^  ^
         |  read = 1
         write - 1 = 0, write = 1
```

## Step by step

Each round compares `nums[read]` with `nums[write - 1]`.

```text
read=1  nums[1]=0  vs last kept 0   same: skip
        [0, 0, 1, 1, 1, 2]    write=1

read=2  nums[2]=1  vs last kept 0   new: nums[1] = 1, write -> 2
        [0, 1, 1, 1, 1, 2]    write=2

read=3  nums[3]=1  vs last kept 1   same: skip
        [0, 1, 1, 1, 1, 2]    write=2

read=4  nums[4]=1  vs last kept 1   same: skip
        [0, 1, 1, 1, 1, 2]    write=2

read=5  nums[5]=2  vs last kept 1   new: nums[2] = 2, write -> 3
        [0, 1, 2, 1, 1, 2]    write=3
```

The function returns `3`. The first three slots are `0, 1, 2`; the leftover `1, 1, 2` after them is ignored.

## Why it works

`read` is always at or ahead of `write`, so copying `nums[read]` into `nums[write]` never overwrites a value we still need. Because the array is sorted, a value that differs from the last kept one cannot appear again later, so each distinct value is copied exactly once and in order.

## Where it goes wrong

Comparing against `nums[read - 1]` instead of `nums[write - 1]` looks similar but is a different test. After copies have happened, `nums[read - 1]` may be a stale value from the old layout rather than the last kept value.

```text
[0, 1, 2, 1, 1, 2]  after the last copy, write = 3
   kept part: [0, 1, 2]     nums[write - 1] = 2 is the last kept value
   leftovers: [1, 1, 2]     stale; nums[read - 1] could point into these
```

Starting `write` at 0 would let `nums[0]` be compared with a non-existent `nums[-1]`, which in Python silently reads the last element. An array with one element never enters the loop and returns 1.

## Cost

Time O(n), one pass. Space O(1), in place.
