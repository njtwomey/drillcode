---
title: Prefix sums and hashing
area: Hashing and counting
topics: [Array, Hash]
problems:
  - range-sum-query-immutable
  - subarray-sum-equals-k
  - contiguous-array
  - subarray-sums-divisible-by-k
  - car-pooling
  - random-pick-with-weight
related: [prefix-and-suffix-passes, seen-before-insert, sliding-window, index-as-hash]
---

## Reach for it when

- The question is about a contiguous subarray with a given sum, a given remainder, or equal counts of two kinds of item.
- The array has negative numbers or zeros, so a `sliding-window` cannot be trusted. Shrinking and growing a window only works when the sum moves one way.
- Many range-sum queries arrive for the same array.
- Many range updates ("add `x` to every slot from `a` to `b`") are applied, and only the final values are read.
- The same question is asked on a tree path ("downward path with sum k"): `path-sum-iii` runs this on the current root path, with a hash map that is undone on the way back up.

## Setup

- `prefix`: the sum of `nums[:i + 1]` so far. The sum of `nums[a..b]` is `prefix[b] - prefix[a - 1]`, so a subarray ending here has a wanted sum when an earlier prefix equals `prefix - k`.
- `seen = {0: 1}`: a map from a prefix value to how many earlier prefixes had it. The entry `0: 1` is the empty prefix. It lets a subarray that starts at index 0 be found.
- For a longest span, `seen` maps each prefix value to its first index, and starts as `{0: -1}`.
- Order inside the loop: update `prefix`, look up, then insert. Invariant: `seen` holds only prefixes strictly before the current one.
- For range queries, build the prefix list once with a leading `0`, so `prefix[i]` is the sum of `nums[:i]`.
- For range updates, build a difference array: add at the start of a range, subtract just past its end. A running sum of the differences recovers the values.

## Template

```python
def count_subarrays_with_sum(nums, k):
    seen = {0: 1}
    prefix = 0
    result = 0
    for num in nums:
        prefix += num
        result += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return result


assert count_subarrays_with_sum([1, 1, 1], 2) == 2
assert count_subarrays_with_sum([1, -1, 0], 0) == 3
assert count_subarrays_with_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
assert count_subarrays_with_sum([], 0) == 0
```

## What it removes

The O(n^2) loop over every start and end, and the failure of the sliding window on negative numbers. Equal prefixes mean the stretch between them sums to zero, so a lookup replaces the inner loop. A prefix array also turns each range-sum query from O(n) to O(1). The difference array is the inverse: it turns each range update from O(length) into two writes.

## Pitfalls

- Forgetting the seed. Without `{0: 1}`, `[1, 1, 1]` with `k = 2` finds only one subarray, because the one that starts at index 0 has no earlier prefix to match.
- Inserting the current prefix before the lookup. When `k = 0` the prefix finds itself and every element counts as an empty subarray.
- Storing an index and overwriting it, when counting. Several earlier prefixes can share a value (zeros, negatives), and each one is a different subarray, so a count is needed. For a longest span, do the opposite: keep only the first index, because overwriting it shortens the answer.
- Using a sliding window when values can be negative. `[1, -1, 5]` with `k = 5` is missed because the sum is not monotone.
- Taking a remainder in a language where `%` can be negative. In Python `-1 % 3 == 2`, so a negative prefix lands in the same bucket as `k - 1`. In C++ or Java a fix-up like `((x % k) + k) % k` is needed.
- Off by one in the prefix list. With a leading `0`, the sum of `nums[left..right]` is `prefix[right + 1] - prefix[left]`, not `prefix[right] - prefix[left]`.
- In a difference array, subtracting at the end of the range instead of just past it. If the trip ends at stop `to` and the passengers leave there before anyone boards, the range is `[start, to)`: add at `start`, subtract at `to`.

## Variants

- Plain prefix array: `range-sum-query-immutable` builds `self.prefix = [0]` and appends the running sum. `sumRange` returns `self.prefix[right + 1] - self.prefix[left]`. No hash map is needed, since the range is given.
- Count with a target: `subarray-sum-equals-k` keeps `count_of`, a map from prefix sum to how many times it occurred, seeded with `{0: 1}`. It adds `count_of.get(prefix - k, 0)` before inserting the current prefix.
- Longest span with equal counts: `contiguous-array` maps 0 to -1, so equal numbers of 0s and 1s mean a subarray sum of 0. `balance` is the running sum and `first_seen` maps a balance to the earliest index, seeded with `{0: -1}`. When `balance` is already in `first_seen`, the span is `i - first_seen[balance]`. Otherwise the index is stored. The map holds the first index and is not overwritten.
- Divisible by k: `subarray-sums-divisible-by-k` keeps `prefix = (prefix + num) % k` and counts how many earlier prefixes have the same remainder, since equal remainders mean the stretch between is a multiple of `k`. `count_of` is seeded with `{0: 1}`. It relies on Python giving a result in `[0, k)` for negative numbers. The map has at most `k` keys.
- Range updates, then one read: `car-pooling` builds a difference array `change` over stops. Each trip adds `passengers` at `start` and subtracts them at `to`. A running `load` over `change` is the number of passengers in the car after each stop, and it must never exceed `capacity`. This is the inverse of a prefix sum.
- Tree version: `path-sum-iii` is the same idea on a tree. The map counts the prefix sums on the current root path, is seeded with `{0: 1}`, and the entry is decremented when the call returns so sibling subtrees do not see each other. It is listed under the tree techniques, not here.
- Weights to ranges: `random-pick-with-weight` stores `self.prefix = list(accumulate(w))` and `self.total = self.prefix[-1]`. Index `i` owns the integer targets in `(prefix[i-1], prefix[i]]`, a block of size `w[i]`. A uniform `target = random.randint(1, self.total)` then lands in block `i` with probability `w[i] / total`. No hash map; the prefix array is searched with `bisect_left`, as in `binary-search-shapes`.

## Worked example

Problem: `subarray-sum-equals-k`

A running prefix sum is paired with a map of how often each earlier prefix occurred.

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count_of = {0: 1}
        prefix = 0
        result = 0
        for num in nums:
            prefix += num
            result += count_of.get(prefix - k, 0)
            count_of[prefix] = count_of.get(prefix, 0) + 1
        return result
```

`count_of` plays the part of the template's `seen`, and `prefix` and `result` are the same. The lookup of `prefix - k` comes before the insert, so with `k = 0` the empty subarray is not counted. The seed `{0: 1}` is the empty prefix. The solution adds the whole tally, not 1, because several earlier prefixes can share one value.
