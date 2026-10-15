## The idea

A rearrangement of `s1` is any string with the same letters in the same counts. So we are looking for a stretch of `s2` that is exactly `len(s1)` long and has the same letter counts as `s1`. Sorting every candidate substring would be slow. Instead, keep a count of letters for the current stretch and nudge it as the stretch slides one place right.

## Set-up

- `m` is `len(s1)`; the stretch is always `m` characters wide. If `s1` is longer than `s2`, nothing can match, so return `False` at once.
- `need` is 26 counts for `s1`. It never changes.
- `window` is 26 counts for the last `m` characters of `s2` seen so far.

The invariant: after processing index `i`, `window` holds the counts for the up-to-`m` characters ending at `i`.

```text
s1 = "ab"            need   : a=1 b=1  (rest 0)
s2 = "eidbaooo"      window : all zero
```

## Step by step

Each round adds `s2[i]`. If `i >= m`, the window is too wide, so subtract `s2[i - m]`. Then compare the two arrays. Only letters a, b, d, e, i are shown nonzero.

```text
i  adds  drops  window contents   window == need?
0   e     -      e                no
1   i     -      e i              no
2   d     e      i d              no
3   b     i      d b              no
4   a     d      b a              yes -> return True
```

The match is `"ba"` at positions 3 and 4, a rearrangement of `"ab"`.

## Why it works

The window always covers exactly the last `m` characters. Adding the new one and removing the oldest updates the counts in constant time, with no recount. Two strings of equal length are rearrangements of each other precisely when their letter counts match, so a matching `window` means a matching substring.

## Where it goes wrong

- Subtracting the wrong character: it must be `s2[i - m]`, the one that just fell out of the left end. Using `i - m + 1` keeps the window one too narrow.
- Right letters, wrong counts:

```text
s1 = "aa", s2 = "aba"      need: a=2
i=1  window: a=1 b=1       not equal
i=2  add a, drop s2[0]     window: a=1 b=1   not equal
```

Both windows hold an `a`, but never two. Matching the set of letters is not enough, the counts must be equal.

## Cost

Time O(n) for `s2` of length n. Each step does O(1) updates and compares two arrays of 26, which is constant. Space O(1): two arrays of 26.
