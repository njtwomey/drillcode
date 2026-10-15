---
title: Read and write pointers
area: Pointers and windows
topics: [Two pointers, Array]
problems:
  - move-zeroes
  - remove-duplicates-from-sorted-array
  - sort-colors
  - longest-common-prefix
related: [opposite-ends, seen-before-insert]
---
## Reach for it when
- You must filter or partition an array in place.
- The statement asks for O(1) extra space.
- The array is sorted and duplicates must collapse to one copy each.
- Kept elements must stay in their original order (or, for three values, the array must end up grouped).

## Setup
- `write = 0`: the next slot a kept element goes to. Invariant: `nums[:write]` is the kept prefix, in original order.
- `read`: the loop index, `for read in range(len(nums))`. Everything before it has been examined.
- When `nums[read]` is kept, swap it (or, when the tail does not matter, copy it) into `nums[write]` and do `write += 1`.
- For three-way partitions, use three pointers instead: `lo`, `mid`, `hi`. Invariant: `nums[:lo]` holds the first class, `nums[lo:mid]` the second, `nums[mid:hi + 1]` is unexamined, and `nums[hi + 1:]` holds the third class.

## Template
```python
def keep_in_front(nums, keep):
    write = 0
    for read in range(len(nums)):
        if keep(nums[read]):
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return write
```

## What it removes
It removes the second array. Instead of building a filtered copy and copying it back, the swap moves kept elements forward and lets the rest drift to the back, in one pass. When `write == read` the swap is a no-op on the same slot, which is harmless. The three-pointer form removes the counting pass of a counting sort.

## Pitfalls
- In `remove-duplicates-from-sorted-array`, comparing `nums[read]` with `nums[write]` instead of `nums[write - 1]`. The slot at `write` is the next free one and may hold a stale value, so a new value is mistaken for a duplicate (`[1, 2, 2]` returns 1 instead of 2). Also, returning the last kept index instead of `write`, which is the count, off by one on every input.
- Starting `write` and `read` at 0 for the sorted-unique case. `nums[0]` is always kept, so `write = 1` and `read` starts at 1; at 0 the first element is compared with the slot before it.
- Copying instead of swapping in `move-zeroes`, then forgetting the fill pass: the tail keeps stale values (`[1, 0, 2]` becomes `[1, 2, 2]`).
- In `sort-colors`, advancing `mid` after swapping with `hi`: the value swapped in was never examined, so a 2 or 0 is left in the wrong zone (`[2, 0, 1]` ends unsorted).
- Using `<` instead of `<=` in `while mid <= hi`: the last unexamined element is skipped (`[1, 0]` ends unsorted).
- Advancing only `lo` on a 0: `mid` then re-examines the settled value and `lo` and `mid` drift out of step (`[0, 1]` loops wrongly). Advance both, because what sits at `lo` is a known 1 or `mid` itself.

## Variants
- Two-pointer partition (`move-zeroes`): the template. The solution swaps rather than copies, so zeros drift to the back and one pass suffices.
- Copy-forward on sorted input (`remove-duplicates-from-sorted-array`): `write = 1` is the length of the unique prefix. A value is kept when `nums[read] != nums[write - 1]`, because sorted order makes any difference from the last kept value a new value. It is copied, not swapped, since the tail beyond `write` is ignored. Return `write`.
- Three-way partition (`sort-colors`): the Dutch national flag. The solution names the pointers `lo`, `mid`, `hi`. A 0 swaps with `lo`, and both `lo` and `mid` advance. A 1 advances `mid`. A 2 swaps with `hi` and only `hi` moves.
- Column scan, not a filter (`longest-common-prefix`): a vertical scan over `first = strs[0]`. For each index `i` and character `c`, every `s` in `strs` is checked with `i == len(s) or s[i] != c`. The length test comes first so a short string stops the scan before indexing. On the first failure it returns `first[:i]`. If no column fails, `first` itself is the answer. Listed here as the nearest pointer-over-array page. The shared idea is one index advanced in lockstep over several sequences, stopping at the first disagreement.
- Merge into the free tail: see `opposite-ends` for `merge-sorted-array`, where the write index `k` starts at the end so nothing unread is overwritten.

## Worked example
Problem: `sort-colors`

Three zones are grown in place by one scan.

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1
```

`mid` plays the role of `read`, and `lo` plays the role of `write` for the zeros. A 0 is swapped into `lo`. What was at `lo` is a known 1 (or `mid` itself), so the value now at `mid` is settled and both advance. A 2 is swapped with `hi`. The value that arrives at `mid` is unexamined, so `mid` stays and `hi` shrinks.
