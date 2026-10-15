## The idea

Keep a window `s[left..right]` with no repeated letters. When the new letter at `right` already appears inside the window, the window is no good. The slow fix is to remove letters from the left one by one until the duplicate is gone. The quick fix is to remember where each letter last appeared and jump `left` straight past that earlier copy.

## Set-up

- `seen` maps each character to its most recent index.
- `left` is the start of the window; `right` is the loop index.
- `best` is the longest window length seen.

Invariant: `s[left..right]` contains no duplicates after each round.

## Step by step

`s = "abba"`.

```text
right=0  c='a'  not seen.
  index: 0 1 2 3
  char:  a b b a
         ^
       left,right          seen = {a:0}      len 1   best 1

right=1  c='b'  not seen.
  index: 0 1 2 3
  char:  a b b a
         L R                seen = {a:0, b:1} len 2   best 2

right=2  c='b'  seen at 1, so left = max(0, 1 + 1) = 2.
  index: 0 1 2 3
  char:  a b b a
             L,R            seen = {a:0, b:2} len 1   best 2

right=3  c='a'  seen at 0, so left = max(2, 0 + 1) = 2.   (stale, no move)
  index: 0 1 2 3
  char:  a b b a
             L R            seen = {a:3, b:2} len 2   best 2
```

The answer is 2.

## Why it works

For the window to stay duplicate-free, `left` has to be just past the latest earlier copy of `c`. Jumping there directly is the smallest move that restores the invariant, and every letter between the old and new `left` is simply dropped from consideration. `seen` never needs cleaning because stale entries are harmless, as the next section shows.

## Where it goes wrong

The `max(left, ...)` is essential. At `right=3` the entry for `a` is 0, which sits to the left of the window. Without `max`, `left` would move backward:

```text
Wrong: left = seen['a'] + 1 = 1

  index: 0 1 2 3
  char:  a b b a
           L   R       window "bba", len 3  -- contains two b's
```

That would report 3, which is wrong.

## Cost

Time O(n): `right` moves once across the string and `left` only moves forward. Space O(min(n, alphabet size)) for `seen`.
