---
title: Prefix and suffix passes
area: Hashing and counting
topics: [Array]
problems:
  - product-of-array-except-self
  - best-time-to-buy-and-sell-stock
related: [seen-before-insert, opposite-ends, prefix-sums-and-hashing]
---

## Reach for it when

- The answer at each position depends on everything to its left and everything to its right.
- Division or an O(n^2) double loop is ruled out.
- A running aggregate (product, sum, minimum, maximum) of the elements before the current one is enough.

## Setup

- `n = len(nums)` and `result = [1] * n` (or `[0] * n`). The output array doubles as storage for the prefix quantity.
- `prefix = 1`, updated in a left-to-right pass. Invariant: before index `i` is processed, it holds the aggregate of `nums[:i]`.
- `suffix = 1`, updated in a right-to-left pass. Invariant: before index `i` is processed, it holds the aggregate of `nums[i + 1:]`.
- Extra space is O(1) beyond the output.

## Template

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result


assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
```

## What it removes

The O(n^2) loop that recomputes the left and right aggregates for every position, and the division trick, which fails on zeros. Each pass reuses the running value from the previous index. Carrying `suffix` as one variable removes the second array.

## Pitfalls

- Updating the running value before writing it. If `prefix *= nums[i]` comes first, `result[i]` includes `nums[i]` and the answer is wrong for every index.
- Mixing the order between the passes. Both passes must write or multiply before folding in `nums[i]`; if one folds first, that index includes its own element.
- Starting `prefix` or `suffix` at 0 for a product. Everything becomes 0. Start at the identity of the operation.
- Using division when the input has zeros. One zero gives a division by zero; the two-pass version needs no special case.

## Variants

- Excluding the current element: `product-of-array-except-self` writes `prefix` into `result[i]` before folding in `nums[i]`, in both passes.
- Running minimum as a prefix pass: `best-time-to-buy-and-sell-stock` keeps `lowest`, the minimum of the earlier prices, and takes `price - lowest` at each step. It needs one pass because only the left side matters.
- Prefix sums for range queries: when queries ask for a sum over `nums[left..right]`, store every prefix and subtract. See `prefix-sums-and-hashing` for `range-sum-query-immutable` and for combining prefixes with a hash map.
- Both sides at once: `trapping-rain-water` needs the tallest bar on each side. Its catalogue solution uses two pointers and running `left_max` and `right_max` instead of two arrays. See `opposite-ends`.

## Worked example

Problem: `product-of-array-except-self`

Two passes over one output array.

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result
```

This is the template. `result[i] = prefix` happens before `prefix *= nums[i]`, so index `i` is excluded. The second pass multiplies into the stored prefix, so `result[i]` ends as left product times right product.
