## The idea

Every letter of the note must be matched by a different letter in the magazine, so what matters is how many of each letter we have, not where they sit. Count the letters available, then spend them one by one while reading the note. If you ever try to spend a letter you have none of, the note cannot be built.

## Set-up

- `counts` is a list of 26 integers, one per lowercase letter, indexed by `ord(ch) - 97` (so `a` is slot 0, `b` slot 1, and so on). The input is lowercase only, so a fixed list is smaller and quicker than a dictionary and keeps space constant.
- A length check comes first. If the note is longer than the magazine, there cannot be enough letters, so we return `False` at once.

Invariant: after the counting pass, `counts[k]` is how many copies of letter `k` remain unspent. While spending, a negative entry means overdrawn.

## Step by step

Note `"aa"`, magazine `"ab"` (the lengths are equal, so the early check passes). Only the nonzero slots are shown.

```text
Count the magazine:
  'a'  counts: a=1
  'b'  counts: a=1  b=1

Spend the note:
  'a'  a: 1 -> 0       still fine
  'a'  a: 0 -> -1      below zero: no 'a' left, return False
```

And a passing case, note `"aa"`, magazine `"aab"`:

```text
After counting:   a=2  b=1
Spend 'a':        a=1
Spend 'a':        a=0
note finished, never went negative: return True
```

An extra letter in the magazine (the `b`) is never used, which is allowed.

## Why it works

Reading the note, each letter takes one unit from its own slot. A slot goes negative exactly when the note asks for more copies of that letter than the magazine contains. Different letters never interfere with each other, so checking each slot on its own is enough. If no slot ever goes below zero, every letter had enough copies.

## Where it goes wrong

Counting the note instead of the magazine and comparing at the end works, but is easy to get backwards. Another slip is checking the sign only after the whole loop; the code checks right after each decrement, which fails early. An empty note never enters the second loop and returns `True`.

```text
ransomNote = ""         magazine = "abc"      -> True (nothing to build)
ransomNote = "abc"      magazine = "ab"       -> False by length alone
```

## Cost

Time O(m + n) for magazine length m and note length n. Space O(1): the list always has 26 slots, whatever the input size.
