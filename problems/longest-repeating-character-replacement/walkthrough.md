## The idea

Pick a window of the string. To make it a single repeated letter you keep its most common letter and change the rest. So the edits needed are `window length - count of the most common letter`. A window is acceptable when that is at most `k`.

That turns the problem into "find the longest acceptable window", which is a sliding window. The twist is that you never have to recompute the true maximum count when the window shrinks.

## Set-up

- `window` counts each letter inside `[left, right]`.
- `max_count` is the highest count seen in any window so far. It is never lowered.
- `left` is the window start; `best` is the longest valid length seen.

Invariant: the window never gets smaller. It either grows, or slides by one step.

## Step by step

`s = "AABABBA"`, `k = 1`. Each round adds `s[right]`, updates `max_count`, and if `length - max_count > k` moves `left` one step.

```text
 r  ch  window counts  max_count  len  len-max  action        window   best
 0  A   A1             1          1    0        ok            A        1
 1  A   A2             2          2    0        ok            AA       2
 2  B   A2 B1          2          3    1        ok            AAB      3
 3  A   A3 B1          3          4    1        ok            AABA     4
 4  B   A3 B2          3          5    2 >1     drop s[0]=A   ABAB     4
 5  B   A2 B3          3          5    2 >1     drop s[1]=A   BABB     4
 6  A   A2 B3          3          5    2 >1     drop s[2]=B   ABBA     4
```

(The counts shown for rounds 4 to 6 are before the drop.) The answer is 4.

After round 4 the window `ABAB` really has a top count of 2, yet `max_count` still says 3. That is the stale value. It makes later checks slightly too generous, but a window can only grow when a letter's count truly passes `max_count`, so the stale value can never produce a longer answer than exists.

## Why it works

`best` only increases when `max_count` increases, because the window slides at a fixed size otherwise. `max_count` increases only when some window really has that many of one letter. So the final `best` is backed by a genuine window that needed at most `k` edits.

## Where it goes wrong

The single `if` is deliberate: the window slides by one step instead of shrinking until it is valid, so its size never drops. That is what makes the stale `max_count` safe. Also, decrement `window[s[left]]` before moving `left`, otherwise you decrement the wrong letter.

## Cost

Time O(n): `right` and `left` each move at most n steps. Space O(1): the dictionary holds at most 26 letters.
