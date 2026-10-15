---
title: Lookup before insert
area: Hashing and counting
topics: [Hash]
problems:
  - two-sum
  - contains-duplicate
  - valid-anagram
  - group-anagrams
  - ransom-note
  - longest-consecutive-sequence
  - valid-sudoku
  - top-k-frequent-elements
related: [prefix-and-suffix-passes, heap-patterns]
---

## Reach for it when

- You need pairs that reach a target.
- You need to find duplicates.
- You need to group items by something canonical.
- The question is "have I met this before", or "how many of each".

## Setup

- `seen = {}` or `seen = set()`. Invariant: it holds only the elements strictly before the current one.
- For each element, look up its partner (or itself) in `seen` first, then insert the element. Checking first stops an element pairing with itself.
- For counting, use a `Counter`, or a 26-element list indexed by `ord(c) - ord('a')` when the input is lowercase letters.

## Template

```python
def pair_with_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []


assert pair_with_sum([2, 7, 11, 15], 9) == [0, 1]
assert pair_with_sum([3, 3], 6) == [0, 1]
assert pair_with_sum([3, 2, 4], 6) == [1, 2]
```

## What it removes

The inner loop that compares each element with every other. A hash lookup is O(1) on average, so n pairs of comparisons become n lookups, at the cost of O(n) memory. Looking only at earlier elements also means each pair is found once, when its second member arrives.

## Pitfalls

- Inserting before checking. In `two-sum`, `[3, 2, 4]` with target 6 returns `[0, 0]`.
- Using a list as a dict key. It raises `TypeError`; freeze it as a `tuple`, as in `group-anagrams`.
- Wrong sudoku box index. It is `(r // 3) * 3 + c // 3`; `r // 3 + c // 3` collides.
- Counting from every value in `longest-consecutive-sequence`. A run of length n is then walked n times and the work is O(n^2).
- Forgetting that a set drops duplicates. Counts need a dict or a `Counter`.

## Variants

- Complement lookup: `two-sum` maps value to index and looks up `target - num`.
- Membership test: `contains-duplicate` returns on the first repeat. Sorting and comparing neighbours is the O(1) space alternative.
- Frequency comparison: `valid-anagram` compares two `Counter`s.
- Canonical key: `group-anagrams` keys a dict by a 26-count `tuple`. `''.join(sorted(word))` also works but costs O(L log L) per word.
- Spend a budget: `ransom-note` counts the magazine into 26 slots, then decrements per note letter. A count below zero means failure.
- Run starts: `longest-consecutive-sequence` puts values in a set and counts upward only from values whose predecessor `num - 1` is absent, so each run is walked once.
- One set per unit: `valid-sudoku` keeps a set for each row, column and box, and fails when a digit is already in any of its three.
- Bucket by frequency: `top-k-frequent-elements` makes `buckets[count]` a list of values. Counts are at most n, so the top k come from the high end in O(n), where a heap is O(n log k).

## Worked example

Problem: `contains-duplicate`

The simplest form of the pattern.

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```

`seen` is the template's set. The membership test comes before `seen.add(num)`, so `seen` holds only earlier elements when the test runs. The first element that is already there is the second copy of a value.
