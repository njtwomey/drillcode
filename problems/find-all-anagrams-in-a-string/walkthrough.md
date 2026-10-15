## The idea

Two strings are anagrams when they have the same letter counts. So we want every spot in `s` where a stretch of length `len(p)` has the same counts as `p`.

Recounting each stretch from scratch costs O(n * m). But consecutive stretches overlap almost completely. Sliding right by one drops a single letter on the left and picks up a single letter on the right. So keep one running count and update it in constant time per step.

## Set-up

- `m = len(p)` is the window size. If `p` is longer than `s` there is nothing to find, and we return early.
- `need` is the 26 letter counts of `p`. It never changes.
- `window` is the 26 letter counts of the current stretch of `s`.
- `result` collects start indices.

Invariant: after adding `s[i]` and removing the letter that fell off, `window` holds the counts of the last `m` characters ending at `i`.

```text
s = "abab"   p = "ab"   m = 2

need   = { a:1, b:1 }          (all other letters 0)
window = { }
```

Only non-zero counts are drawn below; the real arrays have 26 cells.

## Step by step

```text
i=0  add 'a'.   window = {a:1}                 window not full yet (i < m-1)

i=1  add 'b'.   window = {a:1, b:1}
     i >= 1, window == need: match, start = 1 - 2 + 1 = 0       result [0]
     [a b] a b

i=2  add 'a'.   window = {a:2, b:1}
     i >= m, remove s[0] = 'a':  window = {a:1, b:1}
     match, start = 2 - 2 + 1 = 1                               result [0, 1]
      a [b a] b

i=3  add 'b'.   window = {a:1, b:2}
     remove s[1] = 'b':          window = {a:1, b:1}
     match, start = 3 - 2 + 1 = 2                               result [0, 1, 2]
      a  b [a b]
```

The answer is `[0, 1, 2]`. Overlapping matches are fine because the window just keeps sliding.

## Why it works

The window only changes by one letter in and one letter out, so the update is exact and the counts are always right. Comparing two length-26 lists is a fixed cost, not dependent on `m` or `n`. Two stretches have the same counts exactly when they are anagrams of each other.

## Where it goes wrong

Two off-by-ones live here.

- Removal starts when `i >= m`, not `i >= m - 1`. At `i = m - 1` the window has just reached size `m` and nothing should leave yet.
- The recorded start is `i - m + 1`, the left end of the window, not `i`.

Comparing before the window is full would match a short prefix against `need` only by luck, and the guard `i >= m - 1` prevents it.

## Cost

Time O(n): each character is added once and removed once, and each comparison is 26 cells. Space O(1): two arrays of 26 integers, regardless of input size (the output list aside).
