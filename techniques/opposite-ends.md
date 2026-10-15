---
title: Two pointers from opposite ends
area: Pointers and windows
topics: [Two pointers]
problems:
  - two-sum-ii-input-array-is-sorted
  - valid-palindrome
  - container-with-most-water
  - 3sum
  - trapping-rain-water
related: [read-write-pointers, sliding-window]
---
## Reach for it when
- The input is sorted and you need a pair (or a triple) that hits a target.
- You must check a symmetry, such as a palindrome.
- The quantity depends on both ends, such as width times the smaller height.
- A brute-force answer would try every pair, and each comparison tells you that one end can never be part of a better answer.

## Setup
- `left = 0`: the lowest index still in play. Everything before it has been ruled out.
- `right = len(items) - 1`: the highest index still in play. Everything after it has been ruled out.
- Loop `while left < right`. Invariant: if an answer exists, it lies within `[left, right]`.
- Extra state, when the problem needs it: `best` or `total` for an accumulated answer, `left_max` and `right_max` for running maxima from each side.

State the discarding argument in one sentence before coding it. "If the sum is too small, nothing paired with `left` can work, so `left += 1`." "Moving the taller wall cannot increase the area, so move the shorter one."

## Template
```python
def pair_with_sum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

## What it removes
It replaces the nested loop over all pairs with one pass, O(n) instead of O(n²). It also replaces the hash map in two-sum: sortedness lets you discard one end per step, so no extra memory is needed. In `trapping-rain-water` it removes the two prefix-maximum arrays.

## Pitfalls
- Skipping duplicates with `if` instead of `while`: three equal values in a row yield a repeated triplet in `3sum`.
- Moving only one pointer after a hit in `3sum`: the same pair is found again. Move both, then skip equal values on both sides.
- Skipping duplicates without the `left < right` guard: the inner `while` runs past the other pointer and raises an `IndexError` or skips valid values.
- `<=` instead of `<` in the loop condition: the pointers meet on one element and it gets paired with itself (wrong answer for a pair sum such as `[3]` with target 6).
- Forgetting the 1-indexed output in `two-sum-ii-input-array-is-sorted`: off by one on every answer.
- In `valid-palindrome`, skipping junk with a `while` that lacks the `left < right` guard: an all-punctuation string runs the pointers off the ends.

## Variants
- Pair with a target (`two-sum-ii-input-array-is-sorted`): too small moves `left`, too big moves `right`.
- Symmetry check (`valid-palindrome`): both pointers move together on a match. Non-alphanumeric characters are skipped one side per iteration, so each iteration still moves a pointer.
- Greedy on the smaller side (`container-with-most-water`): measure, then move the shorter wall. Any container that keeps it is capped by its height and is narrower.
- Anchor plus pair (`3sum`): sort, fix `i` and skip repeated anchor values, break once `nums[i] > 0`, then run the pair search on the rest looking for `-nums[i]`.
- Carry a running maximum per side (`trapping-rain-water`): `left_max` and `right_max`. If `height[left] < height[right]`, some bar on the right is at least as tall as anything on the left, so the water at `left` depends only on `left_max`. It is decided and `left` can move. The solution compares the heights at the pointers, not the two maxima.

## Worked example
Problem: `3sum`

The outer loop fixes the smallest value at `i`. The inner loop is the template with a three-term total, plus duplicate skipping after each hit.

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return result
```

`left, right = i + 1, n - 1` is the template's setup, restricted to the part of the array after the anchor. `total` is the same sum as in the template, with `nums[i]` added. Too small moves `left`, too big moves `right`. A hit moves both pointers, then the two `while` loops skip values equal to the ones just used. The anchor skip `nums[i] == nums[i - 1]` does the same job for the outer loop.
