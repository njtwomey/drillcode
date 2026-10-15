---
title: Index as hash
area: Hashing and counting
topics: [Array]
problems:
  - find-all-numbers-disappeared-in-an-array
  - first-missing-positive
  - find-the-duplicate-number
  - missing-number
related: [seen-before-insert, fast-slow-pointers, bit-tricks, prefix-sums-and-hashing]
---

## Reach for it when

- The array has `n` slots and the values are drawn from `1..n` (or `0..n`), or the values you care about are.
- The question is "which numbers are missing", "which are repeated", or "what is the smallest missing positive".
- The statement asks for O(1) extra space, so a `set` is ruled out.
- The input may be modified in place.

## Setup

- The value `v` belongs at index `v - 1` (or at index `v` when the range is `0..n`). The array is its own hash table, with the identity as the hash function.
- Cyclic placement: loop `i` over the array, and while `nums[i]` is in range and its home slot does not already hold it, swap it home. Invariant: after the loop every in-range value that exists sits at its home slot.
- Sign marking: for each value `v`, negate `nums[abs(v) - 1]`. Invariant: a negative slot means that its index plus one was seen. Read values through `abs()`.
- Afterwards, scan once: the first slot that is wrong (not `i + 1`, or still positive) names a missing number.

## Template

```python
def first_missing(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


assert first_missing([3, 4, -1, 1]) == 2
assert first_missing([7, 8, 9, 11, 12]) == 1
assert first_missing([1, 2, 3]) == 4
assert first_missing([1, 1]) == 2
```

## What it removes

The O(n) extra memory of a `set` or a count array. There are `n` slots and at most `n` values of interest, so the slots can record presence. Each swap puts one value home for good, so the `while` loop does at most `n` swaps in total and the whole pass stays O(n).

## Pitfalls

- Looping on `nums[i] != i + 1` instead of `nums[nums[i] - 1] != nums[i]`. A duplicate would swap with itself forever (`[1, 1]` never ends).
- Using `nums[i]` as the swap target after the first assignment. `nums[i], nums[nums[i] - 1] = ...` changes `nums[i]` before the index is used. Compute `j = nums[i] - 1` first.
- Forgetting the range test. `0`, negatives and values above `n` have no home slot, and indexing with them raises `IndexError` or wraps around to the wrong slot.
- In sign marking, writing `nums[index] = -nums[index]`. A repeated value flips the sign back and the number looks missing. Write `-abs(nums[index])`.
- In sign marking, reading `nums[i]` without `abs()`. An earlier step may have negated it, which yields a negative index.
- Returning `n` rather than `n + 1` when every slot is right. `[1, 2, 3]` has the answer 4.
- Forgetting that the input is changed. If it must stay intact, use a `set` (the `solution_set.py` files do) or copy first.

## Variants

- Sign marking: `find-all-numbers-disappeared-in-an-array` takes each `num`, computes `index = abs(num) - 1`, and sets `nums[index] = -abs(nums[index])`. The slots still positive afterwards are the missing numbers, reported as `i + 1`. It runs in O(n) time and O(1) extra space. The values are all in `1..n`, so no range test is needed.
- Cyclic placement: `first-missing-positive` swaps each value `v` in `1..n` into index `v - 1`. The loop stops when the target slot already holds the value, which also handles duplicates. A second scan returns the first `i + 1` where `nums[i] != i + 1`, or `n + 1`. Values outside `1..n` are ignored, because the answer cannot exceed `n + 1`. `solution_set.py` is the O(n)-space alternative that probes `candidate = 1, 2, ...` in a `set`.
- Indices as pointers: `find-the-duplicate-number` treats `nums[i]` as the next index of a linked list and finds the cycle entrance with `fast-slow-pointers`. It does not change the array, so it also fits when the input is read-only.
- Presence by arithmetic: `missing-number` has values `0..n` and one is absent. It XORs every index and value together, starting from `n`; what is left is the missing number. The sum version subtracts `sum(nums)` from `n * (n + 1) // 2`. See `bit-tricks`.

## Worked example

Problem: `first-missing-positive`

Each value is moved to the slot it belongs in, then one scan finds the first slot that is wrong.

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
```

The `while` is the template's placement loop. The range test `1 <= nums[i] <= n` skips values with no home, and `nums[nums[i] - 1] != nums[i]` stops on a duplicate. `j` is computed before the swap, as the pitfall says. The second loop is the scan, and `n + 1` is the answer when every slot holds its own value.
