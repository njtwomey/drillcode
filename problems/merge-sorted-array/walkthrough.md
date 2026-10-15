## The idea

`nums1` has empty space at its end, exactly the size of `nums2`. If you merge from the front, writing the smallest value into slot 0 would overwrite a real value in `nums1` that you have not used yet. You would need a copy.

Merge from the back instead. The largest remaining value belongs in the last free slot, and that slot is empty (or already consumed), so nothing unread gets destroyed. No extra array is needed.

## Set-up

- `i = m - 1` points at the last unmerged real element of `nums1`.
- `j = n - 1` points at the last unmerged element of `nums2`.
- `k` is the slot being filled, from `m + n - 1` down to `0`.
- Invariant: everything to the right of `k` is final, and slots `0..i` still hold their original `nums1` values.

```text
nums1  [1, 2, 3, 0, 0, 0]      nums2  [2, 5, 6]
              ^ i                            ^ j
                       ^ k
```

## Step by step

Each round compares `nums1[i]` with `nums2[j]` and writes the larger at `k`. On a tie, `nums2` wins.

```text
k=5  3 vs 6 -> write 6 from nums2, j moves left
     nums1 [1, 2, 3, 0, 0, 6]    i=2  j=1

k=4  3 vs 5 -> write 5 from nums2, j moves left
     nums1 [1, 2, 3, 0, 5, 6]    i=2  j=0

k=3  3 vs 2 -> write 3 from nums1, i moves left
     nums1 [1, 2, 3, 3, 5, 6]    i=1  j=0

k=2  2 vs 2 -> tie, write 2 from nums2, j moves left
     nums1 [1, 2, 2, 3, 5, 6]    i=1  j=-1
```

At `k=1`, `j < 0`, so the loop breaks. The remaining `1, 2` in front are already where they belong. The result is `[1, 2, 2, 3, 5, 6]`.

## Why it works

The write slot `k` is always at or to the right of `i`, because `k = i + j + 1` and `j >= -1`. So a write never lands on an unread `nums1` element. Each step places the largest value still unplaced, so the tail fills with the sorted order. When `nums2` is done, the leftover `nums1` prefix is already sorted and in its final place.

## Where it goes wrong

- Merging from the front. That overwrites `nums1` values you still need.
- Using `nums1[i] > nums2[j]` without checking `i >= 0`. When `nums1` runs out first, `i` is `-1` and the index would wrap to the last element.
- Breaking when `nums1` runs out instead of when `nums2` does. If `i < 0`, the rest of `nums2` still has to be copied; the `i >= 0` check sends those steps to the else branch.

## Cost

Time O(m + n): each step places one value. Space O(1): only the indices, since all writes go into `nums1`.
