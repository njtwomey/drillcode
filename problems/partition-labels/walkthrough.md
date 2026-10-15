## The idea

Cut the string into as many pieces as possible so that each letter shows up in only one piece. If a letter appears in a piece, that piece must reach all the way to the letter's last occurrence. So the first piece must stretch at least to the last occurrence of every letter in it, and that stretching can chain: a letter inside the stretched part may force it further.

Greedy: remember where each letter last appears, walk left to right while pushing the forced end out, and cut the instant the walk reaches it.

## Set-up

- `last = {c: i for i, c in enumerate(s)}`: the final index of each letter.
- `start`: the first index of the current piece.
- `end`: the farthest index the current piece is forced to reach. Invariant: no letter in `s[start..i]` occurs after `end`.
- `result`: piece lengths.

```text
s = "abcabdee"

index:   0 1 2 3 4 5 6 7
char:    a b c a b d e e

last:    a=3  b=4  c=2  d=5  e=7
```

## Step by step

For each index `i`: `end = max(end, last[c])`; if `i == end`, record `end - start + 1` and set `start = i + 1`.

```text
i=0  a  last=3  end=3
i=1  b  last=4  end=4
i=2  c  last=2  end=4
i=3  a  last=3  end=4
i=4  b  last=4  end=4   i == end -> cut, length 4-0+1 = 5, start=5

i=5  d  last=5  end=5   i == end -> cut, length 5-5+1 = 1, start=6
i=6  e  last=7  end=7
i=7  e  last=7  end=7   i == end -> cut, length 7-6+1 = 2, start=8
```

```text
 a b c a b | d | e e
 0 1 2 3 4   5   6 7
 length 5    1    2
```

The result is `[5, 1, 2]`. `end` is never reset, because `max` makes it jump forward again on its own.

## Why it works

A cut at `i` is legal only when no letter in the prefix of the piece reappears later, which is exactly `i == end` (the farthest last occurrence of anything seen in this piece). Cutting earlier would split a letter. Cutting later would just merge two pieces that could be separate, so cutting at the first legal spot gives the most pieces.

## Where it goes wrong

- Cutting when you see the last occurrence of the first letter only. In `abab` the first `a` ends at 2 but `b` extends the piece to 3, so the answer is `[4]`, not `[3, 1]`.
- Forgetting `max`. Without it a later letter with an earlier last index could pull `end` backwards.
- Off-by-one on the length: it is `end - start + 1`.

```text
s = "abab"       last: a=2, b=3
i=0 a end=2
i=1 b end=3     (extended)
i=2 a end=3
i=3 b end=3     i == end -> one piece of length 4
```

## Cost

Time O(n): one pass to build `last`, one to cut. Space O(1) because the alphabet is fixed (at most 26 letters).
