---
title: Expand around the centre
area: Pointers and windows
topics: [String, Two pointers]
problems:
  - longest-palindromic-substring
  - palindromic-substrings
related: [opposite-ends]
---
## Reach for it when
- The question is about palindromic substrings, longest or counted.
- A DP table over all `(i, j)` pairs would work but you want O(1) extra space.

## Setup
- A palindrome mirrors around its centre. There are `2n - 1` centres: `n` on characters (odd length) and `n - 1` between characters (even length).
- For each centre, start `left` and `right` on it: `(i, i)` for odd, `(i, i + 1)` for even.
- Loop `while left >= 0 and right < n and s[left] == s[right]`, then `left -= 1` and `right += 1`. Invariant: the span strictly inside `left` and `right` is already a palindrome.
- When the loop stops, `left` and `right` are one step past the palindrome. The last valid span is `left + 1 .. right - 1`, with length `right - left - 1`.
- `best` (or `count`): the answer carried across centres.

## Template
```python
def longest_palindrome(s):
    n = len(s)
    best_lo, best_hi = 0, 0

    def expand(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(n):
        for lo, hi in (expand(i, i), expand(i, i + 1)):
            if hi - lo > best_hi - best_lo:
                best_lo, best_hi = lo, hi
    return s[best_lo:best_hi + 1]
```

## What it removes
It removes the DP table. Each of the `2n - 1` centres is expanded directly, so time is O(n²) as with the table, but space is O(1). It also removes the need to test every substring for being a palindrome, which would cost O(n³).

## Pitfalls
- Forgetting the even centres: `"abba"` is answered `"a"`, because no odd centre sees it.
- Reading the span after the loop without undoing the last step: the result includes the mismatched characters on each side. Return `left + 1` and `right - 1`.
- Comparing lengths computed as `right - left` when the span is inclusive: the off-by-one is harmless only when both sides are measured the same way. Compare `hi - lo` with `best_hi - best_lo` consistently.
- Expanding with `if` instead of `while`: only the immediate neighbours are checked.
- Checking `s[left] == s[right]` before the bounds: an `IndexError` at the string edge (or a silent wrap with `left = -1`).

## Variants
- Track the best span (`longest-palindromic-substring`): a helper `expand(left, right)` returns the inclusive bounds. The caller tries `expand(i, i)` and `expand(i, i + 1)` for each `i` and keeps the longest.
- Count every success (`palindromic-substrings`): each successful step of the loop is one more palindromic substring, so `count += 1` goes inside the `while`. The solution loops `center in range(2 * n - 1)` and derives `left = center // 2` and `right = left + center % 2`, so odd and even centres are one loop.

## Worked example
Problem: `palindromic-substrings`

Every match of the outer pair is exactly one more palindrome, so counting goes inside the loop.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0
        for center in range(2 * n - 1):
            left = center // 2
            right = left + center % 2
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
        return count
```

Even `center` values give `right == left` (odd length), odd values give `right == left + 1` (even length). `left` and `right` are the template's pointers, and the `while` is the same expansion. Because the invariant says the inside is already a palindrome, each iteration that passes the check adds one to `count`.
