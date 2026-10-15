## The idea

Every palindrome mirrors around a centre. For odd length the centre is a character, for even length it is the gap between two characters. If we try every centre and push outward while both sides match, we meet every palindrome in the string.

That is O(n²) in the worst case, but it needs no table and no extra memory. A DP over all `(i, j)` pairs would use O(n²) space for the same time.

## Set-up

- `best_lo`, `best_hi` are the inclusive bounds of the best palindrome so far. They start at `0, 0`, because any single character qualifies.
- `expand(left, right)` grows outward while `s[left] == s[right]`, then returns the bounds of the palindrome it found.
- For each index `i` we try two centres: `expand(i, i)` for odd length, `expand(i, i + 1)` for even length. That is all `2n - 1` centres.

## Step by step

Take `s = "cbbd"`. Brackets mark the span returned.

```text
i=0   odd  (0,0): c        -> (0,0)   span 0
      even (0,1): c vs b   -> (1,0)   empty, span -1
i=1   odd  (1,1): b, then c vs b stops -> (1,1)   span 0
      even (1,2): b == b, then c vs d stops
                   c [b b] d  -> (1,2)   span 1  new best
i=2   odd  (2,2): b, then b vs d stops -> (2,2)
      even (2,3): b vs d   -> (3,2)   empty
i=3   odd  (3,3) -> (3,3);  even (3,4) -> (4,3) empty
```

The best is `(1, 2)`, so the answer is `s[1:3]`, which is `"bb"`.

Here is the even expansion at `i=1` in detail:

```text
 index   0  1  2  3
 char    c  b  b  d
            L  R           b == b, step out
         L        R        c vs d, stop
            ^^^^^          expand returns (left + 1, right - 1) = (1, 2)
```

## Why it works

A palindrome's centre is unique, and growing outward from that centre succeeds exactly as far as the palindrome extends. Trying every centre therefore finds the longest one. Comparing `right - left` against `best_hi - best_lo` compares lengths minus one on both sides, so the off-by-one cancels.

## Where it goes wrong

- Forgetting the even centres misses answers like `"bb"`.
- `expand` stops one step past the palindrome, so it must return `left + 1, right - 1`. A failed even expansion gives an empty span like `(3, 2)`; its negative span never beats the best, which is fine.

## Cost

Time O(n²): 2n - 1 centres, each expanding up to O(n) (think of a string of identical letters). Space O(1) beyond the returned slice. Manacher's algorithm gets O(n) but is rarely needed.
