## The idea

A palindrome mirrors around its centre. Instead of testing every substring (O(n^3)), pick each possible centre and grow outward while the two ends match. Each successful step outward is one more palindromic substring, so we count as we grow.

Centres come in two kinds: on a character (odd length like `aba`) and between two characters (even length like `abba`). A string of length `n` has `n` of the first and `n - 1` of the second, so `2n - 1` centres.

## Set-up

- `count`: running total of palindromic substrings.
- `center` runs over `range(2 * n - 1)`. Index `center` maps to `left = center // 2` and `right = left + center % 2`. Even `center` values start with `left == right` (a character); odd ones start with `right = left + 1` (the gap after a character).
- Invariant inside the loop: `s[left+1..right-1]` is already a palindrome (empty at the start), so if `s[left] == s[right]` the substring `s[left..right]` is one more.

```text
s = "aba"      n = 3, centres 0..4

centre:  0     1     2     3     4
left:    0     0     1     1     2
right:   0     1     1     2     2
        (a)   (a|b) (b)   (b|a) (a)
```

## Step by step

```text
centre 0   left=0 right=0   a == a   count=1
           left=-1          stop
centre 1   left=0 right=1   a != b   stop
centre 2   left=1 right=1   b == b   count=2
           left=0 right=2   a == a   count=3   ("aba")
           left=-1          stop
centre 3   left=1 right=2   b != a   stop
centre 4   left=2 right=2   a == a   count=4
           left=1 right=3   right out of range, stop
```

The four palindromes are `a`, `b`, `aba`, `a`, so the answer is `4`.

## Why it works

Every palindromic substring has a unique centre, so counting by centre counts each once. For a given centre, once an outer pair fails to match, no wider substring around that centre can be a palindrome, so stopping is safe. The inner part is already a palindrome whenever the loop is at an outer pair, so one comparison per step is enough.

## Where it goes wrong

- Only handling odd centres, which misses `abba`, `aa` and so on.
- Computing `right` as `left + 1` for every centre. Only the odd `center` values start in a gap.
- Forgetting the bounds checks, so `s[-1]` silently reads the last character.

```text
s = "aa"
  odd centres only:   a, a            -> 2   (wrong)
  with gap centre:    a, a, aa        -> 3
```

## Cost

Time O(n^2): `2n - 1` centres, each growing up to O(n) steps; a string of one repeated letter reaches that bound. Space O(1).
