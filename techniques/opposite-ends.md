---
title: Two pointers from opposite ends
area: Pointers and windows
topics: [Two pointers]
problems:
  - two-sum-ii-input-array-is-sorted
  - valid-palindrome
  - container-with-most-water
  - 3sum
  - 3sum-closest
  - 4sum
  - squares-of-a-sorted-array
  - boats-to-save-people
  - trapping-rain-water
related: [read-write-pointers, sliding-window]
---
## Reach for it when
- The input is sorted and you need a pair (or a triple) that hits a target.
- You must check a symmetry, such as a palindrome.
- The quantity depends on both ends, such as width times the smaller height.
- The largest or smallest values sit at the two ends, and the output is built from the outside in (sorted squares, pairing the heaviest with the lightest).
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
- `<=` instead of `<` in the loop condition of a pair search: the pointers meet on one element and it gets paired with itself (wrong answer for a pair sum such as `[3]` with target 6). `boats-to-save-people` is the exception and needs `<=`: when `left == right` one person is still waiting, and `<` would leave that last person without a boat (`[5]` with limit 5 gives 0 instead of 1).
- In `3sum-closest`, starting `best` at `0` or at a huge number that is not a real sum. Start it at `nums[0] + nums[1] + nums[2]`, a sum that exists, so the first comparison is fair.
- In `4sum`, skipping the second value with `nums[j] == nums[j - 1]` alone. It must be `j > i + 1 and ...`, or `[2, 2, 2, 2, 2]` with target 8 loses its only answer, because `j = i + 1` is compared with the anchor `i`.
- In `squares-of-a-sorted-array`, filling `result` from the front. The smallest square is in the middle, not at an end, so the front fill needs a sort afterwards.
- Forgetting the 1-indexed output in `two-sum-ii-input-array-is-sorted`: off by one on every answer.
- In `valid-palindrome`, skipping junk with a `while` that lacks the `left < right` guard: an all-punctuation string runs the pointers off the ends.

## Variants
- Pair with a target (`two-sum-ii-input-array-is-sorted`): too small moves `left`, too big moves `right`.
- Symmetry check (`valid-palindrome`): both pointers move together on a match. Non-alphanumeric characters are skipped one side per iteration, so each iteration still moves a pointer.
- Greedy on the smaller side (`container-with-most-water`): measure, then move the shorter wall. Any container that keeps it is capped by its height and is narrower.
- Anchor plus pair (`3sum`): sort, fix `i` and skip repeated anchor values, break once `nums[i] > 0`, then run the pair search on the rest looking for `-nums[i]`.
- Closest instead of exact (`3sum-closest`): sort, fix `i`, run the pair search on the rest, and keep `best`, the sum with the smallest `abs(total - target)`. Too small moves `left`, too big moves `right`. An exact hit returns at once. No duplicate skipping is needed, since the answer is one number.
- One more anchor (`4sum`): two nested anchors `i` and `j`, with the repeat-skip at each level (`i > 0`, `j > i + 1`), then the `3sum` pair search on `left, right = j + 1, n - 1`. After a hit both pointers move and equal values on both sides are skipped.
- Output from the outside in (`squares-of-a-sorted-array`): the largest square is at `left` or `right`, so `result` is filled from the back with the larger `abs`, and only the pointer that was used moves. This is a merge of two sorted runs, read from the large end.
- Pair by greedy (`boats-to-save-people`): sort, then the heaviest person at `right` always takes a boat. The lightest at `left` joins if `people[left] + people[right] <= limit`; otherwise `right` goes alone. `right -= 1` and `count += 1` happen every round, and the loop is `while left <= right`.
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
