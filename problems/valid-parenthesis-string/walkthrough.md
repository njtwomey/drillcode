## The idea

Without stars this is the classic counter: add one for `(`, subtract one for `)`, never dip below zero, finish at zero. A `*` breaks the counter, because it could be a `(`, a `)` or nothing, and the right choice may depend on what comes later.

Trying all three choices for every star is exponential. The shortcut is to stop deciding. Instead of one count, track every open-count that some choice of stars could have produced so far. That set is always a contiguous range, so two numbers describe it.

## Set-up

- `lo` is the smallest number of open parentheses reachable so far (every star used as `)` where possible).
- `hi` is the largest (every star used as `(`).

Both start at 0: before reading anything, exactly zero are open.

```text
reachable open counts:   [lo, hi] = [0, 0]
```

## Step by step

Each character moves the range:

- `(` shifts both ends up by one.
- `)` shifts both ends down by one.
- `*` widens it: `lo` goes down (as `)`), `hi` goes up (as `(`); empty is the values in between.

After each character, if `hi < 0` we fail, and `lo` is clamped to 0. Trace `"(*))"`:

```text
char   lo  hi   after clamp   meaning
start   0   0    [0, 0]
 (      1   1    [1, 1]       one open, no choice
 *      0   2    [0, 2]       star as ')' gives 0, as '(' gives 2
 )     -1   1    [0, 1]       lo clamped from -1
 )     -1   0    [0, 0]       lo clamped, hi still ok
```

At the end `lo == 0`, so zero open parentheses is achievable: return `True`. (Read it as `(` `(` `)` `)`.)

## Why it works

Any count between `lo` and `hi` is reachable, because changing a single star from `)` to empty to `(` changes the count by one at a time. So the range really is the full set of possibilities. The string is valid exactly when 0 is in the final range. Since `hi` is the most optimistic count, `hi < 0` means even the best case has an unmatched `)`, and nothing later can fix it. Since counts are never allowed below zero, `lo` only needs to be the smallest non-negative one.

## Where it goes wrong

Forgetting the clamp. A negative `lo` is not a real state; it means "this star should have been empty". Without the clamp, `"*("` slips through:

```text
"*("  without clamp          with clamp
 *    lo=-1 hi=1             lo=0  hi=1
 (    lo= 0 hi=2             lo=1  hi=2
end   lo==0 -> True (wrong)  lo==1 -> False (correct)
```

A star cannot close a `(` that comes after it.

## Cost

Time O(n): one pass. Space O(1): two integers.
