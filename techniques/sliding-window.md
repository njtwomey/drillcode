---
title: Sliding window
area: Pointers and windows
topics: [Sliding window]
problems:
  - longest-substring-without-repeating-characters
  - longest-repeating-character-replacement
  - minimum-window-substring
  - minimum-size-subarray-sum
  - max-consecutive-ones-iii
  - permutation-in-string
  - find-all-anagrams-in-a-string
  - sliding-window-maximum
related: [monotonic-stack, opposite-ends]
---
## Reach for it when
- The target is a contiguous subarray or substring.
- The question is "longest", "shortest" or "count" under a constraint.
- The window has a fixed length and you ask whether its contents match something (an anagram, a permutation).
- The constraint can be checked incrementally, and it only gets worse as the window grows (or only better as it shrinks).

## Setup
- `left = 0`: the start of the window. The window is `s[left..right]`.
- `right`: the end of the window, from `for right, c in enumerate(s)`.
- `window`: the contents of the window, as a `dict` or `Counter` of counts (or a map of last positions). Invariant: it describes exactly `s[left..right]`.
- `best`: the answer so far (a length, or a start and length).

Three shapes of loop:
- Longest valid: add `s[right]`. While the window is invalid, remove `s[left]` and do `left += 1`. Then record `right - left + 1`.
- Shortest valid: add `s[right]`. While the window is valid, record it, remove `s[left]` and do `left += 1`.
- Fixed length `m`: add `s[right]`. When `right >= m`, remove `s[right - m]`. Once the window holds `m` items, compare it with the target. No `left` variable is needed; it is `right - m + 1`.

The state can be a number rather than a map: `total` for a sum, `zeros` for a count of one kind of item.

## Template
```python
def longest_with_at_most_k_distinct(s, k):
    window = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        window[c] = window.get(c, 0) + 1
        while len(window) > k:
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

## What it removes
It replaces the O(n²) loop over every start and end with one pass in which `left` and `right` only move forward, so total work is O(n). Each element enters the window once and leaves once. A validity check kept up to date incrementally (a count, a `missing` total) removes the re-scan of the window on each step.

## Pitfalls
- Recording `best` before shrinking in the longest-valid shape: the window is still invalid and the length is too big.
- In the shortest-valid shape, recording after the shrink loop instead of inside it: the window is no longer valid when recorded.
- Removing `s[left]` after `left += 1`: the wrong character is removed and the counts drift.
- Setting `left = seen[c] + 1` without `max(left, ...)` in `longest-substring-without-repeating-characters`: a stale entry left of the window moves `left` backwards and re-admits duplicates (wrong answer on `"abba"`, which gives 3 instead of 2).
- Not deleting zero-count keys when validity is `len(window)`: the window looks bigger than it is.
- In the fixed-length shape, dropping the old item at `right - m` before the window is full, or comparing before it is full. Both give a wrong answer on a short prefix. The reported start is `right - m + 1`, not `right - m`.
- In `permutation-in-string` and `find-all-anagrams-in-a-string`, forgetting that `m > len(s)` leaves nothing to slide over. Return early.
- In `minimum-size-subarray-sum`, a window `while` that is `if`: one removal does not restore the state. Also, returning `best` when it never improved; the solution starts it at `len(nums) + 1` and returns `0` in that case.
- Using the shrink-while-valid shape on input with negative numbers. It only works because every element is positive, which makes the window monotone. With negatives, use `prefix-sums-and-hashing`.
- Using `if` where `while` is needed: one removal does not restore validity, so the window stays invalid.

## Variants
- Jump the left edge (`longest-substring-without-repeating-characters`): keep `seen`, a map from character to last index, and set `left = max(left, seen[c] + 1)` instead of shrinking one step at a time.
- Fixed-size slide with a stale maximum (`longest-repeating-character-replacement`): the window is valid while `length - max_count <= k`. The solution uses `if` rather than `while`, so the window never shrinks, it only slides. `max_count` is never lowered. A stale, too-high value can only keep the window the same size, never inflate it, because the answer grows only when `max_count` really grows.
- Shortest valid with a satisfaction counter (`minimum-window-substring`): `need` starts as the `Counter` of `t`, and `missing` starts as `len(t)`. The window is valid when `missing == 0`, an O(1) check. A count above zero in `need` means the window still lacks that character; negative means surplus. The solution shrinks while the leftmost character is surplus, records, then deliberately drops one needed character to break validity and resume expanding.
- Shortest valid by sum (`minimum-size-subarray-sum`): `total` is the window sum, `best` starts at `len(nums) + 1` as the not-found marker. While `total >= target`, record `right - left + 1`, subtract `nums[left]` and advance `left`. Positive numbers make the sum monotone in the window size.
- Longest with a budget (`max-consecutive-ones-iii`): `zeros` counts the zeros in the window, which are the flips used. While `zeros > k`, move `left` forward and decrement `zeros` when a zero leaves. `best` is recorded after the shrink. Nothing is flipped.
- Fixed window, compare counts (`permutation-in-string`): `need` and `window` are 26-slot lists. Each step adds `s2[i]`, and when `i >= m` removes `s2[i - m]`. It returns `True` when `window == need`. Comparing two lists of 26 is a constant cost.
- Fixed window, collect all matches (`find-all-anagrams-in-a-string`): the same counts, but the check is `i >= m - 1 and window == need`, and the start `i - m + 1` goes into `result`.
- Window maximum (`sliding-window-maximum`): the window slides at fixed size `k`, and a deque of indices holds the candidates. See `monotonic-stack` for the deque form.

## Worked example
Problem: `longest-substring-without-repeating-characters`

The window is `s[left..right]` and holds no repeats. A map of last positions lets `left` jump.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        left = 0
        best = 0
        for right, c in enumerate(s):
            if c in seen:
                left = max(left, seen[c] + 1)
            seen[c] = right
            best = max(best, right - left + 1)
        return best
```

`left`, `right`, `best` and the loop `for right, c in enumerate(s)` are the template's. `seen` plays the part of `window`, but stores the last index instead of a count. The `max(...)` guards against a stale entry that sits left of the window. `best` is recorded after `left` is settled, so the window is valid when measured.
